"""Read assistant messages from Claude Code session files."""

from __future__ import annotations

import json
import os
import platform
import re
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Directory discovery
# ---------------------------------------------------------------------------

def _claude_dir() -> Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(env) if env else Path.home() / ".claude"


def _projects_dir() -> Path:
    return _claude_dir() / "projects"


def _desktop_sessions_dir() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "local-agent-mode-sessions"
    if system == "Windows":
        return Path.home() / "AppData" / "Roaming" / "Claude" / "local-agent-mode-sessions"
    return Path.home() / ".config" / "Claude" / "local-agent-mode-sessions"


def _find_desktop_project_dirs(base: Path, max_depth: int = 8) -> list[Path]:
    results: list[Path] = []

    def walk(directory: Path, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            entries = list(directory.iterdir())
        except (OSError, PermissionError):
            return
        for entry in entries:
            if entry.name in ("node_modules", ".git") or not entry.is_dir():
                continue
            if entry.name == "projects":
                try:
                    for pd in entry.iterdir():
                        if pd.is_dir():
                            results.append(pd)
                except (OSError, PermissionError):
                    pass
            else:
                walk(entry, depth + 1)

    if base.is_dir():
        walk(base, 0)
    return results


def _project_dir_name(cwd: str) -> str:
    return cwd.replace("/", "-")


def _discover_project_dirs() -> list[Path]:
    dirs: list[Path] = []
    projects = _projects_dir()
    if projects.is_dir():
        for entry in projects.iterdir():
            if entry.is_dir():
                dirs.append(entry)
    dirs.extend(_find_desktop_project_dirs(_desktop_sessions_dir()))
    return dirs


def _find_latest_session(project_dir: Path) -> Path | None:
    sessions = sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return sessions[0] if sessions else None


def _find_active_session(cwd: str | None = None) -> Path:
    """Return the session file Claude Code is actively writing to.

    Primary strategy: pick the globally most-recently-modified .jsonl across
    all project directories — Claude Code writes to the session file on every
    message, so the current session always has the freshest mtime.

    CWD validation: if *cwd* is supplied and any of the candidate sessions
    live in a project dir that matches the CWD ancestry, we restrict the
    search to those dirs only.  This prevents collisions when a user has
    multiple concurrent Claude Code windows open in completely different trees.
    """
    all_dirs = _discover_project_dirs()
    if not all_dirs:
        raise FileNotFoundError("No Claude Code project directories found")

    # Dirs that match the CWD ancestry (may be empty)
    cwd_dirs: set[Path] = set()
    if cwd:
        dir_by_name = {d.name: d for d in all_dirs}
        path = Path(cwd).resolve()
        while True:
            candidate = dir_by_name.get(_project_dir_name(str(path)))
            if candidate is not None:
                cwd_dirs.add(candidate)
            parent = path.parent
            if parent == path:
                break
            path = parent

    search_dirs = cwd_dirs if cwd_dirs else set(all_dirs)

    best: Path | None = None
    best_mtime: float = 0.0
    for project_dir in search_dirs:
        for session_file in project_dir.glob("*.jsonl"):
            try:
                mtime = session_file.stat().st_mtime
                if mtime > best_mtime:
                    best_mtime = mtime
                    best = session_file
            except OSError:
                continue

    if best is None:
        raise FileNotFoundError(f"No Claude Code session files found (cwd={cwd})")
    return best


# ---------------------------------------------------------------------------
# Rich turn data model
# ---------------------------------------------------------------------------

@dataclass
class ToolEvent:
    """A single tool call and its result within a turn."""
    name: str
    inputs: dict
    result: str = ""        # stdout / file content / search results
    is_error: bool = False


@dataclass
class RichTurn:
    """A complete assistant turn: text blocks + all tool calls made."""
    texts: list[str] = field(default_factory=list)
    tools: list[ToolEvent] = field(default_factory=list)

    @property
    def had_tool_use(self) -> bool:
        return bool(self.tools)

    def plain_text(self) -> str:
        return "\n\n".join(self.texts)


# ---------------------------------------------------------------------------
# Session parsing
# ---------------------------------------------------------------------------

def _is_tool_result_entry(obj: dict) -> bool:
    content = obj.get("message", {}).get("content", [])
    if isinstance(content, list):
        return any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content)
    return False


_CLI_OUTPUT = re.compile(r"^(preview|pdf|docx|html|md)\s+→\s+\S")


def _extract_rich_turns(session_path: Path) -> list[RichTurn]:
    """Parse session JSONL into RichTurn objects.

    Each turn spans from one real user message to the next.
    Tool results (user entries with tool_result content) are matched back
    to their tool_use calls and stored on the same turn.
    """
    turns: list[RichTurn] = []
    current: RichTurn = RichTurn()
    # call_order: ToolEvents in the order tool_use blocks were encountered
    call_order: list[ToolEvent] = []
    # pending: tool_use_id -> ToolEvent (for result matching)
    pending: dict[str, ToolEvent] = {}

    def _close_turn() -> None:
        # Flush all tools in call order (call_order preserves tool_use sequence)
        for evt in call_order:
            current.tools.append(evt)
        call_order.clear()
        pending.clear()

    with session_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = obj.get("type")

            # ---- user entry ----
            if entry_type == "user":
                content = obj.get("message", {}).get("content", [])
                if isinstance(content, list) and any(
                    isinstance(b, dict) and b.get("type") == "tool_result"
                    for b in content
                ):
                    # Attach results to their ToolEvent objects (already in call_order)
                    for block in content:
                        if not isinstance(block, dict) or block.get("type") != "tool_result":
                            continue
                        tid = block.get("tool_use_id", "")
                        if tid not in pending:
                            continue
                        result_content = block.get("content", "")
                        if isinstance(result_content, list):
                            result_content = "\n".join(
                                b.get("text", "") for b in result_content
                                if isinstance(b, dict) and b.get("type") == "text"
                            )
                        evt = pending.pop(tid)
                        evt.result = str(result_content)
                        evt.is_error = bool(block.get("is_error", False))
                        # Don't append here — _close_turn flushes in call order
                    continue

                # Real user message — close current turn
                _close_turn()
                if current.texts or current.tools:
                    turns.append(current)
                    current = RichTurn()
                continue

            # ---- assistant entry ----
            if entry_type != "assistant":
                continue

            content = obj.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue

            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "text":
                    text = block["text"].strip()
                    if text:
                        current.texts.append(text)
                elif btype == "tool_use":
                    evt = ToolEvent(
                        name=block.get("name", ""),
                        inputs=block.get("input", {}),
                    )
                    tid = block.get("id", "")
                    call_order.append(evt)
                    pending[tid] = evt

    # Flush remaining tools in call order, then close final turn
    _close_turn()
    if current.texts or current.tools:
        turns.append(current)

    return turns


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _is_partial_turn(turn: RichTurn) -> bool:
    """True when the last tool in this turn has no result yet (still in progress)."""
    return bool(turn.tools) and turn.tools[-1].result == ""


def read_session_rich(count: int = 1, cwd: str | None = None) -> list[RichTurn]:
    """Return the last `count` RichTurn objects from the current session."""
    cwd = cwd or os.getcwd()
    session_path = _find_active_session(cwd)

    all_turns = _extract_rich_turns(session_path)
    if not all_turns:
        raise ValueError("No assistant messages found in the current session")

    pool = [
        t for t in all_turns
        if t.texts
        and not _CLI_OUTPUT.match(t.plain_text())
        and not _is_partial_turn(t)       # skip the in-progress turn
    ]

    if not pool:
        raise ValueError("No assistant text found in the current session")

    return pool[-count:]


def read_session(count: int = 1, cwd: str | None = None) -> str:
    """Return last `count` turns as plain Markdown (no tool context)."""
    turns = read_session_rich(count=count, cwd=cwd)
    return "\n\n---\n\n".join(t.plain_text() for t in turns)
