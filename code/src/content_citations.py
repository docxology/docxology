from __future__ import annotations

from html import escape


class ContentCitations:
    """Resolve explicit work identities; never infer authors from a citation key."""

    def __init__(self, works: list[dict]) -> None:
        self.works = {work["citation_key"]: work for work in works}
        if len(self.works) != len(works):
            raise ValueError("Duplicate work citation keys")
        self.used: list[str] = []

    def cite(self, key: str) -> str:
        work = self.works[key]
        authors = work["authors"]
        if not authors or any(not isinstance(name, str) or not name.strip() for name in authors):
            raise ValueError(f"Missing reviewed authors for {key}")
        families = [name.split(",", 1)[0] for name in authors]
        if len(families) > 3:
            label = families[0] + " et al."
        elif len(families) > 1:
            label = ", ".join(families[:-1]) + " & " + families[-1]
        else:
            label = families[0]
        if work.get("contributor_role") == "editor":
            label += ", eds."
        if key not in self.used:
            self.used.append(key)
        return (
            f'<span data-citation-key="{escape(key, quote=True)}">'
            f'<a href="works/{escape(key, quote=True)}.html">{escape(work["title"])}</a>'
            f' ({escape(label)}, {escape(str(work["year"]))})</span>'
        )

    def references(self) -> str:
        items = []
        for key in self.used:
            work = self.works[key]
            source = f'https://doi.org/{work["doi"]}' if work.get("doi") else work["url"]
            contributors = "; ".join(work["authors"]) + (" (eds.)" if work.get("contributor_role") == "editor" else "")
            title_stop = "" if work["title"].endswith((".", "?", "!")) else "."
            items.append(
                f'<li data-reference-key="{escape(key, quote=True)}">'
                f'{escape(contributors.rstrip("."))}. {escape(str(work["year"]))}. '
                f'<a href="works/{escape(key, quote=True)}.html">{escape(work["title"])}</a>{title_stop} '
                f'{escape(work["venue"])}. <a href="{escape(source, quote=True)}">Publication source</a>.</li>'
            )
        return "<ol>" + "\n".join(items) + "</ol>"

    def source_urls(self) -> list[str]:
        return [
            f'https://doi.org/{self.works[key]["doi"]}'
            if self.works[key].get("doi") else self.works[key]["url"]
            for key in self.used
        ]
