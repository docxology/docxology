"""Citation evidence comes from active metadata in the original head."""

from pathlib import Path
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.citation_metadata import CitationHead  # noqa: E402


@pytest.mark.parametrize("lookalike", [
    '<template><meta name="citation_author" content="Fake"></template>',
    '<template><template><meta name="citation_author" content="Fake"></template></template>',
    '<template><head><meta name="citation_author" content="Fake"></head></template>',
    '</head><body><head><meta name="citation_author" content="Fake"></head>',
    '<body><meta name="citation_author" content="Fake">',
    '<!-- <meta name="citation_author" content="Fake"> -->',
    '<script>"<meta name=\"citation_author\" content=\"Fake\">"</script>',
    '<template/><meta name="citation_author" content="Fake"></template>',
    '<template><template/><meta name="citation_author" content="Fake"></template></template>',
    '<script/><meta name="citation_author" content="Fake"></script>',
    '<style/><meta name="citation_author" content="Fake"></style>',
])
def test_inert_and_body_metadata_cannot_fill_citation_gaps(lookalike):
    parser = CitationHead()
    parser.feed('<html><head><meta name="citation_title" content="Real">' + lookalike)
    assert parser.tags == {"citation_title": ["Real"]}


def test_template_end_tags_do_not_close_real_head_and_authors_keep_order():
    parser = CitationHead()
    parser.feed('<head><template></head></template><meta name="citation_author" content="A &amp; B">')
    parser.feed('<meta name="citation_author" content="C" /></head>')
    assert parser.tags == {"citation_author": ["A & B", "C"]}


def test_duplicate_attributes_keep_browser_visible_first_value():
    parser = CitationHead()
    parser.feed('<head><meta name="description" name="citation_title" content="Fake">')
    parser.feed('<meta name="citation_title" content="Real" content="Fake"></head>')
    assert parser.tags == {"citation_title": ["Real"]}
