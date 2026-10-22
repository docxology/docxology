#!/usr/bin/env python3
"""Generate or verify the five high-authority pillar content explainers."""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools.generated_outputs import stale_output_paths, write_output_texts  # noqa: E402
from docxology_tools.build_stamp import footer_build_stamp_html  # noqa: E402
from docxology_tools.site_nav import (  # noqa: E402
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    render_breadcrumb,
    render_nav_domain,
    render_pillar_head,
)

STYLE_BLOCK = """
        .pillar-content{max-width:880px;margin:0 auto;padding:7.5rem 1.5rem 4rem;line-height:1.8;color:var(--text-primary)}
        .pillar-header{margin-bottom:2.5rem;text-align:left;border-bottom:1px solid var(--border);padding-bottom:1.5rem}
        .pillar-header h1{font-family:Georgia,'Times New Roman',serif;font-size:clamp(2.2rem,4.5vw,3.4rem);line-height:1.15;margin-bottom:1rem;color:#fff}
        .pillar-meta{font-size:.9rem;color:var(--text-secondary);display:flex;flex-wrap:wrap;gap:1.5rem;margin-top:1rem}
        .pillar-meta span strong{color:var(--silver-bright)}
        .pillar-content h2{font-family:Georgia,'Times New Roman',serif;font-size:1.75rem;margin:2.5rem 0 1rem;color:#fff;border-bottom:1px solid var(--border);padding-bottom:.5rem}
        .pillar-content h3{font-size:1.25rem;margin:1.8rem 0 .75rem;color:var(--gold)}
        .pillar-content p{margin-bottom:1.4rem;font-size:1.02rem;color:var(--text-secondary)}
        .pillar-content ul,.pillar-content ol{margin:1rem 0 1.5rem 1.5rem;color:var(--text-secondary)}
        .pillar-content li{margin-bottom:.5rem;font-size:1rem}
        .answer-box{background:var(--bg-card);border-left:4px solid var(--gold);padding:1.4rem;margin-bottom:2rem;border-radius:0 8px 8px 0}
        .answer-box p{margin-bottom:0;font-size:1.1rem;color:var(--text-primary);font-weight:500;line-height:1.7}
        .callout-card{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1.4rem;margin:1.5rem 0}
        .callout-card h4{color:var(--gold);margin-bottom:.5rem;font-size:1rem;text-transform:uppercase;letter-spacing:.05em}
        .faq-block{margin-top:3rem;background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:2rem}
        .faq-item{margin-bottom:1.75rem;border-bottom:1px solid var(--border);padding-bottom:1.25rem}
        .faq-item:last-child{margin-bottom:0;border-bottom:none;padding-bottom:0}
        .faq-item h3{font-size:1.15rem;color:#fff;margin-bottom:.5rem}
"""


def render_page(
    filename: str,
    title: str,
    description: str,
    og_image: str,
    eyebrow: str,
    h1_text: str,
    answer_lead: str,
    sections: list[tuple[str, str]],
    faqs: list[tuple[str, str]],
    domain_url: str,
    domain_name: str,
    terms: list[str],
    citation_urls: list[str],
) -> str:
    footer_stamp = footer_build_stamp_html()
    from docxology_tools.title_policy import clip_title  # noqa: PLC0415

    # SERP title budget: only the <title> element carries the clipped form.
    # og:title, twitter:title, and the JSON-LD headline carry the full title;
    # the on-page <h1> stays full-length via h1_text.
    serp_title = clip_title(title)
    canonical_url = f"https://danielarifriedman.com/{filename}"
    faq_items = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"{canonical_url}#article",
                "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
                "headline": title,
                "description": description,
                "url": canonical_url,
                "author": {"@id": "https://danielarifriedman.com/#person"},
                "publisher": {"@id": "https://danielarifriedman.com/#person"},
                "datePublished": "2026-08-14",
                "dateModified": "2026-10-21",
                "citation": citation_urls,
                "inLanguage": "en-US",
                "mainEntityOfPage": canonical_url,
                "about": [{"@type": "DefinedTerm", "name": t} for t in terms],
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": faq_items,
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://danielarifriedman.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Domains", "item": "https://danielarifriedman.com/domains.html"},
                    {"@type": "ListItem", "position": 3, "name": domain_name, "item": canonical_url},
                ],
            },
        ],
    }

    sec_html = []
    for h2, body in sections:
        sec_html.append(f"        <h2>{h2}</h2>\n        {body}")
    sec_str = "\n\n".join(sec_html)

    faq_html = []
    for q, a in faqs:
        faq_html.append(f'            <div class="faq-item"><h3>{q}</h3><p>{a}</p></div>')
    faq_str = "\n".join(faq_html)

    return render_pillar_head(
        title=title,
        serp_title=serp_title,
        description=description,
        canonical_path=filename,
        og_image=og_image,
        style=STYLE_BLOCK,
        jsonld=jsonld,
    ) + f"""<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav_domain(active="domains")}
{render_breadcrumb([("Home", ""), ("Domains", "domains.html"), (domain_name, filename)])}
    <main id="main" class="pillar-content">
        <header class="pillar-header">
            <p class="eyebrow" style="color:var(--gold);font-weight:600;text-transform:uppercase;letter-spacing:0.08em;font-size:0.85rem;margin-bottom:0.5rem;">{eyebrow}</p>
            <h1>{h1_text}</h1>
            <div class="pillar-meta">
                <span>Author: <strong>Daniel Ari Friedman, PhD</strong></span>
                <span>Affiliation: <strong>Active Inference Institute</strong></span>
                <span>Last updated: <strong>2026-10-21</strong></span>
                <span>Domain: <a href="{domain_url}" style="color:var(--gold);">{domain_name}</a></span>
            </div>
        </header>

        <div class="answer-box">
            <p>{answer_lead}</p>
        </div>

{sec_str}

        <section class="faq-block">
            <h2 style="font-size:1.6rem;margin-top:0;border-bottom:none;">Frequently Asked Questions</h2>
{faq_str}
        </section>
    </main>

    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="https://activeinference.institute/">Active Inference Institute</a> · <a href="index.html">danielarifriedman.com</a></p>
        <div class="footer-links">
            <a href="index.html">Home</a>
            <a href="publications.html">Publications</a>
            <a href="domains.html">Domains</a>
            <a href="software.html">Software</a>
            <a href="discovery.html">Discovery</a>
            <a href="cite-verify.html">Cite &amp; Verify</a>
        </div>
        {footer_stamp}
    </footer>
{INTERACTIVE_SCRIPTS}
    {MENU_ESC_SCRIPT}
</body>
</html>
"""


def render_outputs(*, output_root: Path = REPO_ROOT) -> dict[Path, str]:
    """Render every source-owned pillar page without writing it."""
    import json

    from docxology_tools.pillar_content import guides

    works = json.loads((REPO_ROOT / "data/works.json").read_text(encoding="utf-8"))["works"]
    return {output_root / guide["filename"]: render_page(**guide) for guide in guides(works)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if any shared-rendered pillar page is stale")
    args = parser.parse_args()
    outputs = render_outputs()
    stale = stale_output_paths(outputs, repo_root=REPO_ROOT)
    if args.check:
        if stale:
            paths = ", ".join(path.relative_to(REPO_ROOT).as_posix() for path in stale)
            raise SystemExit(f"Stale generated pillar pages: {paths}")
        print(f"checked {len(outputs)} shared-rendered pillar pages")
        return
    write_output_texts(outputs, repo_root=REPO_ROOT)
    for path in outputs:
        print(f"Wrote {path.relative_to(REPO_ROOT)}")

    print("All 5 pillar pages authored and generated successfully!")


if __name__ == "__main__":
    main()
