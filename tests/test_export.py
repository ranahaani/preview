"""Tests for export.py — file generation."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from preview.export import to_html, to_md
from preview.session import RichTurn, ToolEvent


def _turn(text: str) -> RichTurn:
    t = RichTurn()
    t.texts = [text]
    return t


# ---------------------------------------------------------------------------
# to_html
# ---------------------------------------------------------------------------

def test_to_html_creates_file(tmp_path):
    out = tmp_path / "out.html"
    to_html([_turn("# Hello\n\nWorld")], out)
    assert out.exists()
    content = out.read_text()
    assert "<!DOCTYPE html>" in content
    assert "Hello" in content


def test_to_html_includes_copy_button_js(tmp_path):
    out = tmp_path / "out.html"
    to_html([_turn("code here")], out)
    assert "attachCopyButtons" in out.read_text()


def test_to_html_from_plain_text(tmp_path):
    out = tmp_path / "out.html"
    to_html("# Plain Text", out)
    assert "Plain Text" in out.read_text()


def test_to_html_renders_tool_events(tmp_path):
    tool = ToolEvent(name="Bash", inputs={"command": "ls"}, result="file.py")
    turn = _turn("Done.")
    turn.tools = [tool]
    out = tmp_path / "out.html"
    to_html([turn], out)
    assert "bash-command" in out.read_text()


# ---------------------------------------------------------------------------
# to_md
# ---------------------------------------------------------------------------

def test_to_md_writes_plain_text(tmp_path):
    out = tmp_path / "out.md"
    to_md([_turn("## Hello")], out)
    assert out.read_text() == "## Hello"


def test_to_md_joins_turns_with_separator(tmp_path):
    out = tmp_path / "out.md"
    to_md([_turn("First"), _turn("Second")], out)
    content = out.read_text()
    assert "First" in content
    assert "Second" in content
    assert "---" in content


def test_to_md_from_plain_string(tmp_path):
    out = tmp_path / "out.md"
    to_md("raw markdown", out)
    assert out.read_text() == "raw markdown"
