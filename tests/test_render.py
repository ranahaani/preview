"""Tests for render.py — HTML generation."""

from __future__ import annotations

from preview.render import (
    extract_title,
    to_html_body,
    to_rich_html_body,
    _ms_icon,
    _tool_display,
    _render_edit_diff,
    _render_bash_detail,
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
# _ms_icon
# ---------------------------------------------------------------------------

def test_ms_icon_edit():    assert _ms_icon("Edit") == "edit"
def test_ms_icon_write():   assert _ms_icon("Write") == "description"
def test_ms_icon_bash():    assert _ms_icon("Bash") == "terminal"
def test_ms_icon_unknown(): assert isinstance(_ms_icon("Unknown"), str)


# ---------------------------------------------------------------------------
# _tool_display
# ---------------------------------------------------------------------------

def test_tool_display_edit():
    out = _tool_display("Edit", {"file_path": "foo.py"})
    assert "foo.py" in out
    assert "Edit:" in out


def test_tool_display_bash_uses_description():
    out = _tool_display("Bash", {"description": "Run tests", "command": "pytest"})
    assert "Run tests" in out


def test_tool_display_bash_falls_back_to_command():
    out = _tool_display("Bash", {"command": "ls -la"})
    assert "ls -la" in out


def test_tool_display_escapes_html():
    out = _tool_display("Write", {"file_path": "<script>"})
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


# ---------------------------------------------------------------------------
# _render_edit_diff
# ---------------------------------------------------------------------------

def test_render_edit_diff_shows_removed_and_added():
    out = _render_edit_diff({"old_string": "old code", "new_string": "new code", "file_path": "x.py"})
    assert "text-red-600" in out   # removed line colour
    assert "text-green-700" in out  # added line colour
    assert "- old code" in out
    assert "+ new code" in out


def test_render_edit_diff_empty_inputs():
    assert _render_edit_diff({}) == ""


def test_render_edit_diff_only_new():
    out = _render_edit_diff({"new_string": "new", "file_path": ""})
    assert "text-green-700" in out
    assert "text-red-600" not in out


def test_render_edit_diff_line_numbers():
    out = _render_edit_diff({"old_string": "a\nb", "new_string": "c"})
    assert "tabular-nums" in out   # line number span present


# ---------------------------------------------------------------------------
# _render_bash_detail
# ---------------------------------------------------------------------------

def test_render_bash_detail_has_command():
    out = _render_bash_detail({"command": "ls -la"}, "file.py")
    assert "$ ls -la" in out
    assert "bg-inverse-surface" in out


def test_render_bash_detail_has_output():
    out = _render_bash_detail({"command": "ls"}, "file.py\nother.py")
    assert "file.py" in out


def test_render_bash_detail_truncates_long_output():
    out = _render_bash_detail({"command": "ls"}, "x" * 4000)
    assert "truncated" in out


def test_render_bash_detail_empty():
    out = _render_bash_detail({}, "")
    # empty cmd + empty result → just the wrapper div, but no meaningful content
    assert "$ " not in out


# ---------------------------------------------------------------------------
# _highlight_code
# ---------------------------------------------------------------------------

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
    assert "tool-card" in out
    assert "terminal" in out          # material icon name
    assert "bg-inverse-surface" in out  # dark terminal block


def test_rich_body_multiple_turns_have_separator():
    t1 = _make_turn(texts=["First"])
    t2 = _make_turn(texts=["Second"])
    out = to_rich_html_body([t1, t2])
    assert "auto_awesome" in out      # new dashed separator icon


def test_rich_body_single_turn_no_separator():
    t = _make_turn(texts=["Only"])
    out = to_rich_html_body([t])
    assert "auto_awesome" not in out


def test_rich_body_tool_error_class():
    tool = ToolEvent(name="Bash", inputs={"command": "bad"}, result="err", is_error=True)
    turn = _make_turn(tools=[tool])
    out = to_rich_html_body([turn])
    assert "border-error" in out      # new error card border class


def test_rich_body_edit_tool_shows_diff():
    tool = ToolEvent(
        name="Edit",
        inputs={"file_path": "x.py", "old_string": "old", "new_string": "new"},
    )
    turn = _make_turn(tools=[tool])
    out = to_rich_html_body([turn])
    assert "text-red-600" in out
    assert "text-green-700" in out


def test_rich_body_has_header():
    out = to_rich_html_body([])
    assert "Claude Code Response" in out


def test_rich_body_empty_turns():
    out = to_rich_html_body([])
    assert isinstance(out, str)
