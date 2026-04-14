"""Markdown rendering utilities."""

from __future__ import annotations

import re

import markdown as md


def to_html_body(text: str) -> str:
    """Convert raw Markdown text to an HTML fragment."""
    text = re.sub(r"- \[x\]", "- ☑", text)
    text = re.sub(r"- \[ \]", "- ☐", text)

    converter = md.Markdown(
        extensions=["tables", "fenced_code", "nl2br", "sane_lists", "toc"],
    )
    return converter.convert(text)


def extract_title(text: str) -> str:
    """Pull the first heading from Markdown, or return a default."""
    match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    return match.group(1).strip() if match else "Preview"
