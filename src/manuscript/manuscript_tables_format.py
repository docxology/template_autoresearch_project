"""Table-specific formatting helpers for manuscript table builders."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from .manuscript_tokens_format import escape_table_cell


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[str]], caption: str) -> str:
    """Process markdown table."""
    safe_rows = rows or tuple(("N/A",) * len(headers) for _ in range(1))
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in safe_rows:
        lines.append("| " + " | ".join(escape_table_cell(cell) for cell in row) + " |")
    lines.extend(("", f": {caption}"))
    return "\n".join(lines)


def pdf_small_table(headers: Sequence[str], rows: Sequence[Sequence[str]], caption: str) -> str:
    """Process pdf small table.

    Blank lines separate the raw ``\\begingroup``/``\\endgroup`` wrappers from
    the markdown table block. Without them, Pandoc's Beamer longtable writer
    absorbs the trailing ``\\endgroup`` into the table ``\\caption{...}``,
    which corrupts the longtable group/alignment structure ("Missing }" and
    "Misplaced alignment tab" errors). The article-class PDF manuscript is
    unaffected because paragraph breaks do not close a ``\\begingroup``.
    """
    table = markdown_table(headers, rows, caption)
    return "\n".join(("\\begingroup\\footnotesize", "", table, "", "\\endgroup"))


def artifact_reference(path: str) -> str:
    """Cite an artifact without linking the rendered web page to a local worktree."""
    return "N/A" if path in {"", "N/A"} else f"`{Path(path).name}`"
