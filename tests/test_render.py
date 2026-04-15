"""Tests for render.py — HTML generation."""

from __future__ import annotations

from preview.render import (
    extract_title,
    to_html_body,
    to_rich_html_body,
    _tool_icon,
    _tool_label,
    _render_edit_diff,
    _render_bash_detail,
    _highlight_bash,
    _highlight_code,
)
from preview.session import RichTurn, ToolEvent


# ---------------------------------------------------------------------------
# extract_title
# ---------------------------------------------------------------------------

def test_extract_title_h1():
    assert extract_title("# My Title\n\nsome text") == "My Title"


def test_extract_title_fallback():
    assert extract_title("no heading here") == "Claude Response"


def test_extract_title_strips_whitespace():
    assert extract_title("#  Spaced  ") == "Spaced"


# ---------------------------------------------------------------------------
# to_html_body
# ---------------------------------------------------------------------------

def test_to_html_body_renders_heading():
    out = to_html_body("# Hello")
    assert "<h1" in out
    assert "Hello" in out


def test_to_html_body_renders_bold():
    out = to_html_body("**bold**")
    assert "<strong>bold</strong>" in out


def test_to_html_body_renders_code_block():
    out = to_html_body("```python\nprint('hi')\n```")
    assert "print" in out
    assert "highlight" in out  # codehilite css class


def test_to_html_body_checkbox_conversion():
    out = to_html_body("- [x] done\n- [ ] todo")
    assert "☑" in out
    assert "☐" in out


# ---------------------------------------------------------------------------
# _tool_icon
# ---------------------------------------------------------------------------

def test_tool_icon_edit():    assert _tool_icon("Edit") == "✏️"
def test_tool_icon_write():   assert _tool_icon("Write") == "📝"
def test_tool_icon_bash():    assert _tool_icon("Bash") == "▶"
def test_tool_icon_unknown(): assert _tool_icon("Unknown") == "🔧"


# ---------------------------------------------------------------------------
# _tool_label
# ---------------------------------------------------------------------------

def test_tool_label_edit():
    out = _tool_label("Edit", {"file_path": "foo.py"})
    assert "Edited" in out
    assert "foo.py" in out


def test_tool_label_bash_uses_description():
    out = _tool_label("Bash", {"description": "Run tests", "command": "pytest"})
    assert "Run tests" in out


def test_tool_label_bash_falls_back_to_command():
    out = _tool_label("Bash", {"command": "ls -la"})
    assert "ls -la" in out


def test_tool_label_escapes_html():
    out = _tool_label("Write", {"file_path": "<script>"})
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


# ---------------------------------------------------------------------------
# _render_edit_diff
# ---------------------------------------------------------------------------

def test_render_edit_diff_shows_removed_and_added():
    out = _render_edit_diff({"old_string": "old code", "new_string": "new code", "file_path": "x.py"})
    assert "diff-removed" in out
    assert "diff-added" in out


def test_render_edit_diff_empty_inputs():
    assert _render_edit_diff({}) == ""


def test_render_edit_diff_only_new():
    out = _render_edit_diff({"new_string": "new", "file_path": ""})
    assert "diff-added" in out
    assert "diff-removed" not in out


# ---------------------------------------------------------------------------
# _render_bash_detail
# ---------------------------------------------------------------------------

def test_render_bash_detail_has_command():
    out = _render_bash_detail({"command": "ls -la"}, "file.py")
    assert "bash-command" in out
    assert "copy-btn" in out


def test_render_bash_detail_has_output():
    out = _render_bash_detail({"command": "ls"}, "file.py\nother.py")
    assert "bash-output" in out
    assert "file.py" in out


def test_render_bash_detail_truncates_long_output():
    out = _render_bash_detail({"command": "ls"}, "x" * 4000)
    assert "truncated" in out


def test_render_bash_detail_empty():
    assert _render_bash_detail({}, "") == ""


# ---------------------------------------------------------------------------
# _highlight_bash / _highlight_code
# ---------------------------------------------------------------------------

def test_highlight_bash_returns_string():
    out = _highlight_bash("ls -la")
    assert isinstance(out, str)
    assert "ls" in out


def test_highlight_code_python():
    out = _highlight_code("def foo(): pass", filename="foo.py")
    assert "def" in out or "foo" in out


def test_highlight_code_fallback_no_filename():
    out = _highlight_code("some plain text")
    assert isinstance(out, str)


# ---------------------------------------------------------------------------
# to_rich_html_body
# ---------------------------------------------------------------------------

def _make_turn(texts=None, tools=None) -> RichTurn:
    t = RichTurn()
    t.texts = texts or []
    t.tools = tools or []
    return t


def test_rich_body_text_only():
    turn = _make_turn(texts=["## Hello\n\nWorld"])
    out = to_rich_html_body([turn])
    assert "Hello" in out
    assert "response-text" in out


def test_rich_body_with_bash_tool():
    tool = ToolEvent(name="Bash", inputs={"command": "echo hi"}, result="hi")
    turn = _make_turn(texts=["Done."], tools=[tool])
    out = to_rich_html_body([turn])
    assert "tool-event" in out
    assert "bash-command" in out


def test_rich_body_multiple_turns_have_separator():
    t1 = _make_turn(texts=["First"])
    t2 = _make_turn(texts=["Second"])
    out = to_rich_html_body([t1, t2])
    assert "turn-sep" in out


def test_rich_body_single_turn_no_separator():
    t = _make_turn(texts=["Only"])
    out = to_rich_html_body([t])
    assert "turn-sep" not in out


def test_rich_body_tool_error_class():
    tool = ToolEvent(name="Bash", inputs={"command": "bad"}, result="err", is_error=True)
    turn = _make_turn(tools=[tool])
    out = to_rich_html_body([turn])
    assert "tool-error" in out


def test_rich_body_edit_tool_shows_diff():
    tool = ToolEvent(
        name="Edit",
        inputs={"file_path": "x.py", "old_string": "old", "new_string": "new"},
    )
    turn = _make_turn(tools=[tool])
    out = to_rich_html_body([turn])
    assert "diff-removed" in out
    assert "diff-added" in out
