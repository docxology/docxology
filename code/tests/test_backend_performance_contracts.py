"""Performance changes retain metadata, filesystem and generation contracts."""
import json
import os
from pathlib import Path

import pytest
import sys

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools import citation_metadata, generation_plan, redirect_stubs, seo_invariants  # noqa: E402
from docxology_tools.paper_artifacts import PaperResources, SourcePaths  # noqa: E402
import regenerate_all  # noqa: E402


@pytest.mark.parametrize('padding', [0, 1000, 1023, 1024, 2047])
def test_chunked_head_preserves_token_boundaries_and_ignores_long_body(padding):
    class CountingHead(citation_metadata.MetadataHead):
        body_tags = 0

        def handle_starttag(self, tag, attrs):
            if tag == 'p':
                self.body_tags += 1
            super().handle_starttag(tag, attrs)

    head = ('<html><head><!--' + 'x' * padding + '</head>-->'
            '<title>Raw </head><script>hidden</script> text</title>'
            '<template><link rel="canonical" href="https://wrong.example/"></template>'
            '<link href="https://example.com/?x=1&amp;y=2" rel="canonical">'
            '<meta name="citation_title" content="Methods &amp; Evidence">'
            '<meta name="description" content="A &amp; B"></head>')
    document = head + '<body>' + '<p>body</p>' * 10000 + '</body></html>'
    complete = citation_metadata.MetadataHead()
    complete.feed(document)
    complete.close()
    limited = CountingHead.parse(document)
    assert (limited.tags, limited.names, limited.properties, limited.canonicals) == (
        complete.tags, complete.names, complete.properties, complete.canonicals)
    assert limited.canonicals == ['https://example.com/?x=1&y=2']
    assert limited.tags['citation_title'] == ['Methods & Evidence']
    assert limited.body_tags < 300


def test_chunked_head_keeps_implicit_body_boundary():
    document = ('<head><meta name="citation_title" content="First">'
                '<main>body</main><head><meta name="citation_title" content="Wrong"></head>')
    assert citation_metadata.CitationHead.parse(document).tags == {'citation_title': ['First']}


@pytest.mark.parametrize('refresh', ['refresh', 'REFRESH', 'refr&#101;sh', 'r&#x65;fresh'])
def test_redirect_screen_preserves_encoded_refresh(refresh):
    assert redirect_stubs.has_meta_refresh(
        f"<html><body><meta content='0;url=/' http-equiv='{refresh}'></body></html>")


@pytest.mark.parametrize('document', [
    '<!-- <meta http-equiv="refresh" content="0;url=/"> -->',
    '<script>const x = \'<meta http-equiv="refresh" content="0;url=/">\';</script>',
    '<meta http-equiv="refresh" content="">',
    '<p>Ordinary refresh text with no redirect element.</p>',
])
def test_redirect_screen_keeps_semantic_rejections(document):
    assert not redirect_stubs.has_meta_refresh(document)


def paper_fixture(root):
    folder = root / 'papers/2026_Example'
    folder.mkdir(parents=True)
    (folder / 'metadata.json').write_text(json.dumps({'primary_pdf': 'paper.pdf', 'title': 'First'}))
    (folder / 'paper.pdf').write_bytes(b'%PDF-test')
    return folder, SourcePaths({'papers/2026_Example/metadata.json',
                                'papers/2026_Example/paper.pdf', 'data/unrelated.json'})


def test_indexed_source_names_preserve_artifacts_and_reread_metadata(tmp_path):
    folder, snapshot = paper_fixture(tmp_path)
    indexed = PaperResources.load(tmp_path, 'papers/2026_Example/', snapshot)
    ordinary = PaperResources.load(tmp_path, 'papers/2026_Example/', frozenset(snapshot))
    assert indexed == ordinary
    assert snapshot.paper_paths('papers/2026_Example') == (
        'papers/2026_Example/metadata.json', 'papers/2026_Example/paper.pdf')
    (folder / 'metadata.json').write_text(json.dumps({'primary_pdf': 'paper.pdf', 'title': 'Changed'}))
    assert PaperResources.load(tmp_path, 'papers/2026_Example/', snapshot).metadata['title'] == 'Changed'


def test_indexed_names_do_not_cache_file_link_safety(tmp_path):
    folder, snapshot = paper_fixture(tmp_path)
    PaperResources.load(tmp_path, 'papers/2026_Example/', snapshot)
    outside = tmp_path / 'outside.pdf'
    outside.write_bytes(b'%PDF-outside')
    (folder / 'paper.pdf').unlink()
    (folder / 'paper.pdf').symlink_to(outside)
    with pytest.raises(ValueError, match='Unavailable primary_pdf'):
        PaperResources.load(tmp_path, 'papers/2026_Example/', snapshot)


def test_indexed_names_reject_new_hardlink(tmp_path):
    folder, snapshot = paper_fixture(tmp_path)
    PaperResources.load(tmp_path, 'papers/2026_Example/', snapshot)
    os.link(folder / 'paper.pdf', tmp_path / 'retained-copy.pdf')
    with pytest.raises(ValueError, match='Hardlinked'):
        PaperResources.load(tmp_path, 'papers/2026_Example/', snapshot)


def test_page_cache_observes_same_size_rewrite_with_restored_mtime(tmp_path):
    page = tmp_path / 'page.html'
    page.write_text('first')
    seo_invariants.clear_page_cache()
    assert seo_invariants._read(page) == 'first'
    before = page.stat()
    page.write_text('other')
    os.utime(page, ns=(before.st_atime_ns, before.st_mtime_ns))
    assert seo_invariants._read(page) == 'other'


def test_page_cache_bounds_retention_and_rereads_evicted_page(tmp_path, monkeypatch):
    monkeypatch.setattr(seo_invariants, '_PAGE_CACHE_LIMIT', 2)
    seo_invariants.clear_page_cache()
    reads = []
    original = Path.read_text

    def read(path, *args, **kwargs):
        reads.append(path)
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, 'read_text', read)
    paths = [tmp_path / f'{i}.html' for i in range(3)]
    for path in paths:
        path.write_text(path.name)
        assert seo_invariants._read(path) == path.name
    assert seo_invariants._read(paths[0]) == paths[0].name
    assert reads.count(paths[0]) == 2
    assert len(seo_invariants._TEXT_CACHE) == 2
    seo_invariants.clear_page_cache()


def test_page_changed_during_read_is_not_cached(tmp_path, monkeypatch):
    page = tmp_path / 'page.html'
    page.write_text('before')
    seo_invariants.clear_page_cache()
    original = Path.read_text

    def racing_read(path, *args, **kwargs):
        result = original(path, *args, **kwargs)
        if path == page:
            page.write_text('after')
        return result

    with monkeypatch.context() as patch:
        patch.setattr(Path, 'read_text', racing_read)
        with pytest.raises(OSError, match='changed while reading'):
            seo_invariants._read(page)
    assert seo_invariants._read(page) == 'after'


def test_regeneration_cache_miss_observes_input_before_and_after_writer_only(tmp_path, monkeypatch):
    (tmp_path / 'source.txt').write_text('input')
    for relative in ('code/orchestrators/writer.py', 'code/src/shared.py',
                     '.python-version', 'pyproject.toml', 'uv.lock'):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('# fixture source')
    step = generation_plan.GenerationStep('one', 'writer.py', (), (), 'test writer', ('source.txt',))
    original = generation_plan.step_input_fingerprint
    observations = []

    def observe(*args, **kwargs):
        result = original(*args, **kwargs)
        observations.append(result)
        return result

    monkeypatch.setattr(generation_plan, 'step_input_fingerprint', observe)
    result = regenerate_all.run_regeneration(
        repo_root=tmp_path, steps=(step,), runner=lambda *_: (tmp_path / 'output.txt').write_text('output'))
    assert result == (1, 0)
    assert len(observations) == 2
    assert observations[0] is not None and observations[0] == observations[1]


def test_release_runtime_contract_comes_from_project_source(tmp_path, monkeypatch):
    import build_release_integrity as integrity
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/current-counts.json').write_text('{"counts": {}}')
    (tmp_path / 'data/pages-artifact-manifest.json').write_text('{}')
    (tmp_path / 'pyproject.toml').write_text('[project]\nrequires-python = ">=3.16"\nversion = "9.8.7"\n')
    monkeypatch.setattr(integrity, 'REPO_ROOT', tmp_path)
    monkeypatch.setattr(integrity, 'validated_pages_source_commit', lambda _: 'fixture')
    monkeypatch.setattr(integrity, 'scan_public_files', lambda _: [])
    generator = integrity.build_payload()['generator']
    assert generator['python'] == '>=3.16 (pyproject.toml)'
    assert generator['project_version'] == '9.8.7'
