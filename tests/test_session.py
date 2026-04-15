"""Tests for session.py — JSONL parsing and turn extraction."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from preview.session import (
    RichTurn,
    ToolEvent,
    _extract_rich_turns,
    _is_tool_result_entry,
    _project_dir_name,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_session(entries: list[dict]) -> Path:
    """Write JSONL entries to a temp file and return its path."""
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
    for entry in entries:
        tmp.write(json.dumps(entry) + "\n")
    tmp.close()
    return Path(tmp.name)


def _user(content):
    return {"type": "user", "message": {"role": "user", "content": content}}


def _assistant_text(text: str, tool_calls: list[dict] | None = None):
    content = [{"type": "text", "text": text}]
    if tool_calls:
        content.extend(tool_calls)
    return {"type": "assistant", "message": {"role": "assistant", "content": content}}


def _tool_use(tid: str, name: str, inputs: dict):
    return {"type": "tool_use", "id": tid, "name": name, "input": inputs}


def _tool_result(tid: str, result: str, is_error: bool = False):
    return _user([{"type": "tool_result", "tool_use_id": tid, "content": result, "is_error": is_error}])


# ---------------------------------------------------------------------------
# _project_dir_name
# ---------------------------------------------------------------------------

def test_project_dir_name_replaces_slashes():
    assert _project_dir_name("/Users/foo/bar") == "-Users-foo-bar"


def test_project_dir_name_home():
    assert _project_dir_name("/home/user") == "-home-user"


# ---------------------------------------------------------------------------
# _is_tool_result_entry
# ---------------------------------------------------------------------------

def test_is_tool_result_entry_true():
    entry = _tool_result("tid1", "output")
    assert _is_tool_result_entry(entry) is True


def test_is_tool_result_entry_false_for_real_user():
    entry = _user("hello")
    assert _is_tool_result_entry(entry) is False


def test_is_tool_result_entry_false_for_assistant():
    entry = _assistant_text("hi")
    assert _is_tool_result_entry(entry) is False


# ---------------------------------------------------------------------------
# _extract_rich_turns — basic extraction
# ---------------------------------------------------------------------------

def test_single_text_turn():
    session = _make_session([
        _user("hi"),
        _assistant_text("Hello there"),
    ])
    turns = _extract_rich_turns(session)
    assert len(turns) == 1
    assert turns[0].plain_text() == "Hello there"
    assert turns[0].tools == []


def test_multiple_turns_split_by_user():
    session = _make_session([
        _user("first"),
        _assistant_text("Response one"),
        _user("second"),
        _assistant_text("Response two"),
    ])
    turns = _extract_rich_turns(session)
    assert len(turns) == 2
    assert turns[0].plain_text() == "Response one"
    assert turns[1].plain_text() == "Response two"


def test_tool_result_does_not_break_turn():
    """Tool results (user entries with tool_result content) must NOT split turns."""
    session = _make_session([
        _user("do it"),
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Let me check."},
                    _tool_use("t1", "Bash", {"command": "ls"}),
                ],
            },
        },
        _tool_result("t1", "file1.py\nfile2.py"),
        _assistant_text("Done."),
    ])
    turns = _extract_rich_turns(session)
    assert len(turns) == 1
    assert "Let me check." in turns[0].plain_text()
    assert "Done." in turns[0].plain_text()


def test_tool_call_captured_with_result():
    session = _make_session([
        _user("run"),
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Running."},
                    _tool_use("t1", "Bash", {"command": "echo hi"}),
                ],
            },
        },
        _tool_result("t1", "hi"),
        _assistant_text("Done."),
    ])
    turns = _extract_rich_turns(session)
    assert len(turns) == 1
    assert len(turns[0].tools) == 1
    tool = turns[0].tools[0]
    assert tool.name == "Bash"
    assert tool.inputs == {"command": "echo hi"}
    assert tool.result == "hi"
    assert tool.is_error is False


def test_tool_error_flagged():
    session = _make_session([
        _user("run"),
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    _tool_use("t1", "Bash", {"command": "bad"}),
                ],
            },
        },
        _tool_result("t1", "command not found", is_error=True),
    ])
    turns = _extract_rich_turns(session)
    assert turns[0].tools[0].is_error is True


def test_tool_call_order_preserved():
    """Tools must appear in the order they were called, not result-arrival order."""
    session = _make_session([
        _user("go"),
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    _tool_use("t1", "Read",  {"file_path": "a.py"}),
                    _tool_use("t2", "Write", {"file_path": "b.py", "content": "x"}),
                    _tool_use("t3", "Bash",  {"command": "ls"}),
                ],
            },
        },
        # Results arrive in reverse order
        _tool_result("t3", "b.py"),
        _tool_result("t2", ""),
        _tool_result("t1", "content of a"),
    ])
    turns = _extract_rich_turns(session)
    names = [t.name for t in turns[0].tools]
    assert names == ["Read", "Write", "Bash"]


def test_had_tool_use_property():
    session = _make_session([
        _user("x"),
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [_tool_use("t1", "Bash", {"command": "ls"})],
            },
        },
        _tool_result("t1", ""),
    ])
    turns = _extract_rich_turns(session)
    assert turns[0].had_tool_use is True


def test_no_tool_use_property():
    session = _make_session([
        _user("x"),
        _assistant_text("Just text"),
    ])
    turns = _extract_rich_turns(session)
    assert turns[0].had_tool_use is False


def test_multiple_text_blocks_merged():
    session = _make_session([
        _user("x"),
        {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "Part 1"}]}},
        {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "Part 2"}]}},
    ])
    turns = _extract_rich_turns(session)
    assert len(turns) == 1
    assert "Part 1" in turns[0].plain_text()
    assert "Part 2" in turns[0].plain_text()


def test_empty_session():
    session = _make_session([])
    assert _extract_rich_turns(session) == []


def test_only_user_messages():
    session = _make_session([_user("hello"), _user("world")])
    assert _extract_rich_turns(session) == []
