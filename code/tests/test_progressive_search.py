"""Execute the shared client loader across fetch, revision, and data boundaries."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

JS = Path(__file__).resolve().parents[2] / "js" / "search-utils.js"


def run_loader(scenario: str) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node interpreter not available")
    program = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const stamp = '2026-10-02T00:00:00Z';
const work = {id:'work:1', type:'work', title:'Paper', url:'/works/paper.html'};
const video = {id:'video:1', type:'video', title:'Talk', url:'/videos/talk.html'};
const page = {id:'page:1', type:'page', title:'Profile', url:'/about.html', content:'page-only detail'};
const payloads = {
 '/search-index-core.json': {generated_at:stamp, content_segments:['work','video'], items:[work,video,page]},
 '/search-index-content-work.json': {generated_at:stamp, type:'work', items:[{...work, content:'work-only detail'}]},
 '/search-index-content-video.json': {generated_at:stamp, type:'video', items:[{...video, content:'video-only detail'}]}
};
const calls = [];
const failing = new Set();
global.fetch = async (path, options) => {
 calls.push(path);
 assert.equal(options.cache, 'no-cache');
 return {ok:!failing.has(path), status:failing.has(path)?503:200, json:async()=>structuredClone(payloads[path])};
};
"""
    program += "vm.runInThisContext(" + json.dumps(JS.read_text(encoding="utf-8")) + ");\n"
    program += "(async () => {\n" + scenario + "\n})().catch(error => { console.error(error); process.exitCode=1; });\n"
    result = subprocess.run([node, "-"], input=program, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr


def test_core_only_initial_load_and_shared_concurrent_request():
    run_loader("""
const [first, second] = await Promise.all([DocxologySearch.loadCore(), DocxologySearch.loadCore()]);
assert.strictEqual(first, second);
assert.deepEqual(calls, ['/search-index-core.json']);
assert.equal(DocxologySearch.getItems()[2].content, 'page-only detail');
assert.equal(DocxologySearch.getItems()[0].content, undefined);
""")


def test_selected_full_text_segment_is_lazy_deduplicated_and_preserves_metadata():
    run_loader("""
await Promise.all([DocxologySearch.loadContent(['work']), DocxologySearch.loadContent(['work'])]);
assert.deepEqual(calls, ['/search-index-core.json','/search-index-content-work.json']);
assert.equal(DocxologySearch.getItems()[0].content, 'work-only detail');
assert.equal(DocxologySearch.getItems()[1].content, undefined);
assert.equal(DocxologySearch.getItems()[2].content, 'page-only detail');
await DocxologySearch.loadContent();
assert.equal(DocxologySearch.getItems()[1].content, 'video-only detail');
assert.equal(calls.filter(path=>path.includes('content-work')).length,1);
""")


def test_core_failure_does_not_become_a_cached_empty_index():
    run_loader("""
failing.add('/search-index-core.json');
await assert.rejects(DocxologySearch.loadCore(), /503/);
assert.deepEqual(DocxologySearch.getItems(), []);
failing.clear();
assert.equal((await DocxologySearch.loadCore()).length, 3);
assert.equal(calls.length,2);
""")


def test_content_failure_preserves_core_and_can_retry():
    run_loader("""
failing.add('/search-index-content-work.json');
await assert.rejects(DocxologySearch.loadContent(['work']), /503/);
assert.equal(DocxologySearch.getItems()[2].content, 'page-only detail');
failing.clear();
assert.equal((await DocxologySearch.loadContent(['work']))[0].content, 'work-only detail');
""")


def test_deploy_transition_retry_refreshes_core_and_clears_old_segments():
    run_loader("""
const oldStamp = '2026-10-01T00:00:00Z';
payloads['/search-index-core.json'].generated_at = oldStamp;
payloads['/search-index-content-video.json'].generated_at = oldStamp;
await DocxologySearch.loadContent(['video']);
assert.equal(DocxologySearch.getItems()[1].content, 'video-only detail');
await assert.rejects(DocxologySearch.loadContent(['work']), /different index revision/);
assert.equal(calls.filter(path=>path==='/search-index-core.json').length,1);
// The deployment settles before the user retries.
payloads['/search-index-core.json'].generated_at = stamp;
payloads['/search-index-content-video.json'].generated_at = stamp;
const refreshed = await DocxologySearch.loadContent(['work']);
assert.equal(DocxologySearch.getRevision(),stamp);
assert.equal(refreshed[0].content,'work-only detail');
assert.equal(refreshed[1].content,undefined);
assert.equal(calls.filter(path=>path==='/search-index-core.json').length,2);
assert.equal(calls.filter(path=>path==='/search-index-content-work.json').length,2);
await DocxologySearch.loadContent(['video']);
assert.equal(calls.filter(path=>path==='/search-index-content-video.json').length,2);
""")


def test_unsettled_deploy_does_not_start_an_unbounded_reload_loop():
    run_loader("""
payloads['/search-index-core.json'].generated_at = 'older-revision';
await assert.rejects(DocxologySearch.loadContent(['work']), /different index revision/);
await assert.rejects(DocxologySearch.loadContent(['work']), /different index revision/);
assert.equal(calls.filter(path=>path==='/search-index-core.json').length,2);
assert.equal(calls.filter(path=>path==='/search-index-content-work.json').length,2);
""")


def test_late_old_segment_cannot_contaminate_or_clear_new_in_flight_request():
    run_loader("""
const oldStamp = 'older-revision';
payloads['/search-index-core.json'].generated_at = oldStamp;
await DocxologySearch.loadCore();
const originalFetch = global.fetch;
const waitingVideos = [];
global.fetch = (path, options) => {
 if (path !== '/search-index-content-video.json') return originalFetch(path, options);
 calls.push(path);
 return new Promise(resolve=>waitingVideos.push(resolve));
};
const oldVideo = DocxologySearch.loadContent(['video']).catch(error=>error);
await new Promise(resolve=>setImmediate(resolve));
assert.equal(waitingVideos.length,1);
await assert.rejects(DocxologySearch.loadContent(['work']), /different index revision/);
payloads['/search-index-core.json'].generated_at = stamp;
const newVideo = DocxologySearch.loadContent(['video']);
await new Promise(resolve=>setImmediate(resolve));
assert.equal(waitingVideos.length,2);
const videoResponse = revision => ({ok:true,status:200,json:async()=>({
 generated_at:revision,type:'video',items:[{...video,content:revision===stamp?'fresh text':'old text'}]
})});
waitingVideos[0](videoResponse(oldStamp));
assert.match((await oldVideo).message,/superseded/);
const sharedNewVideo = DocxologySearch.loadContent(['video']);
await new Promise(resolve=>setImmediate(resolve));
assert.equal(waitingVideos.length,2);
waitingVideos[1](videoResponse(stamp));
await Promise.all([newVideo,sharedNewVideo]);
assert.equal(DocxologySearch.getItems()[1].content,'fresh text');
assert.equal(calls.filter(path=>path==='/search-index-core.json').length,2);
""")


@pytest.mark.parametrize("mutation", [
    "segment.generated_at = 'older-revision'",
    "segment.type = 'video'",
    "segment.items = []",
    "segment.items.push(segment.items[0])",
    "segment.items[0].id = 'work:missing'",
    "segment.items[0].content = null",
])
def test_rejects_mixed_revision_or_incomplete_segment(mutation):
    run_loader("""
const segment = payloads['/search-index-content-work.json'];
""" + mutation + """;
await assert.rejects(DocxologySearch.loadContent(['work']));
assert.equal(DocxologySearch.getItems()[0].content, undefined);
""")


def test_rejects_duplicate_core_entries_and_unsupported_segment_requests():
    run_loader("""
payloads['/search-index-core.json'].items.push(work);
await assert.rejects(DocxologySearch.loadCore(), /duplicate/);
payloads['/search-index-core.json'].items.pop();
await DocxologySearch.loadCore();
await assert.rejects(DocxologySearch.loadContent(['../private']), /Unsupported/);
assert.deepEqual(calls,['/search-index-core.json','/search-index-core.json']);
""")
