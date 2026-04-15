"""Markdown + rich turn rendering."""

from __future__ import annotations

import html
import re
from datetime import datetime

import markdown as md
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_for_filename
from pygments.util import ClassNotFound


# ---------------------------------------------------------------------------
# Pygments helpers
# ---------------------------------------------------------------------------

_GITHUB_FMT = HtmlFormatter(style="friendly", nowrap=True)


def _highlight_code(code: str, filename: str = "", lang: str = "") -> str:
    """Return syntax-highlighted HTML span sequence (no wrapper div)."""
    try:
        if lang:
            from pygments.lexers import get_lexer_by_name
            lexer = get_lexer_by_name(lang)
        elif filename:
            lexer = get_lexer_for_filename(filename)
        else:
            from pygments.lexers import guess_lexer
            lexer = guess_lexer(code)
    except ClassNotFound:
        lexer = TextLexer()
    return highlight(code, lexer, _GITHUB_FMT)


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def to_html_body(text: str) -> str:
    """Convert raw Markdown text to an HTML fragment."""
    text = re.sub(r"- \[x\]", "- ☑", text)
    text = re.sub(r"- \[ \]", "- ☐", text)
    converter = md.Markdown(
        extensions=["tables", "fenced_code", "codehilite", "nl2br", "sane_lists", "toc"],
        extension_configs={
            "codehilite": {"css_class": "highlight", "guess_lang": True, "use_pygments": True}
        },
    )
    return converter.convert(text)


def extract_title(text: str) -> str:
    match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    return match.group(1).strip() if match else "Claude Response"


# ---------------------------------------------------------------------------
# Tool icon / label helpers
# ---------------------------------------------------------------------------

def _ms_icon(name: str) -> str:
    """Return Material Symbols icon name for a tool."""
    n = name.lower()
    if "edit" in n:   return "edit"
    if "write" in n:  return "description"
    if "read" in n:   return "visibility"
    if "bash" in n:   return "terminal"
    if "glob" in n:   return "folder_open"
    if "grep" in n:   return "search"
    if "agent" in n:  return "smart_toy"
    if "web" in n:    return "public"
    if "task" in n:   return "task_alt"
    if "skill" in n:  return "auto_awesome"
    return "build"


def _icon_color(name: str, is_error: bool) -> str:
    if is_error:
        return "text-error"
    n = name.lower()
    if "edit" in n:   return "text-primary"
    if "write" in n:  return "text-secondary"
    if "bash" in n:   return "text-secondary"
    return "text-outline"


def _tool_display(name: str, inputs: dict) -> str:
    """Return 'Verb: target' label, HTML-escaped."""
    n = name.lower()
    path = inputs.get("file_path") or inputs.get("path") or ""
    if path and ("edit" in n or "write" in n or "read" in n):
        parts = path.replace("\\", "/").split("/")
        short = "/".join(parts[-2:]) if len(parts) > 2 else path
        verb = "Edit" if "edit" in n else ("Write" if "write" in n else "Read")
        return f"{verb}: {html.escape(short)}"
    if "bash" in n:
        desc = inputs.get("description", "") or inputs.get("command", "")
        return f"Bash: {html.escape(str(desc)[:80])}"
    if "glob" in n:
        return f"Glob: {html.escape(inputs.get('pattern', ''))}"
    if "grep" in n:
        return f"Search: {html.escape(inputs.get('pattern', ''))}"
    if "agent" in n:
        kind = inputs.get("subagent_type") or inputs.get("description", "")
        return f"Agent: {html.escape(str(kind)[:60])}"
    return html.escape(name)


# ---------------------------------------------------------------------------
# Tool detail renderers
# ---------------------------------------------------------------------------

def _render_edit_diff(inputs: dict) -> str:
    old = inputs.get("old_string", "")
    new = inputs.get("new_string", "")
    if not old and not new:
        return ""

    rows: list[str] = [
        '<div class="mono text-[13px] leading-6 overflow-x-auto terminal-scroll">'
    ]
    for i, line in enumerate(old.splitlines(), 1):
        rows.append(
            f'<div class="flex bg-red-50 px-4 py-0.5">'
            f'<span class="w-8 text-red-300 select-none text-right pr-2 shrink-0 tabular-nums">{i}</span>'
            f'<span class="text-red-600 font-medium whitespace-pre">- {html.escape(line)}</span>'
            f'</div>'
        )
    for i, line in enumerate(new.splitlines(), 1):
        rows.append(
            f'<div class="flex bg-green-50 px-4 py-0.5">'
            f'<span class="w-8 text-green-300 select-none text-right pr-2 shrink-0 tabular-nums">{i}</span>'
            f'<span class="text-green-700 font-medium whitespace-pre">+ {html.escape(line)}</span>'
            f'</div>'
        )
    rows.append("</div>")
    return "\n".join(rows)


def _render_write_content(inputs: dict) -> str:
    content = inputs.get("content", "")
    path    = inputs.get("file_path", "")
    if not content:
        return ""
    truncated = content[:3000] + ("\n… (truncated)" if len(content) > 3000 else "")
    highlighted = _highlight_code(truncated, filename=path)
    return (
        '<div class="overflow-x-auto terminal-scroll border-t border-outline-variant/10 '
        'bg-surface-container-lowest p-4 max-h-96">'
        f'<pre class="gh-highlight mono text-[13px] leading-relaxed">{highlighted}</pre>'
        '</div>'
    )


def _render_bash_detail(inputs: dict, result: str) -> str:
    cmd = inputs.get("command", "")
    if not cmd and not result:
        return ""
    parts = [
        '<div class="mx-4 mb-4 rounded-lg bg-inverse-surface p-4 text-[13px] mono '
        'leading-relaxed terminal-scroll overflow-x-auto shadow-inner">'
    ]
    if cmd:
        parts.append(f'<div class="text-inverse-on-surface">$ {html.escape(cmd)}</div>')
    if result:
        truncated = result[:3000] + ("\n… (truncated)" if len(result) > 3000 else "")
        parts.append(
            f'<div class="mt-2 text-on-primary-fixed-variant whitespace-pre-wrap">'
            f'{html.escape(truncated)}</div>'
        )
    parts.append("</div>")
    return "\n".join(parts)


def _render_generic_result(result: str) -> str:
    trunc = result[:1000] + ("…" if len(result) > 1000 else "")
    return (
        '<div class="p-4 bg-surface-container border-t border-outline-variant/10 '
        'text-sm mono text-on-surface-variant max-h-48 overflow-y-auto">'
        f'<pre class="whitespace-pre-wrap m-0">{html.escape(trunc)}</pre></div>'
    )


# ---------------------------------------------------------------------------
# Tool event card
# ---------------------------------------------------------------------------

def _render_tool_event(tool) -> str:
    n         = tool.name.lower()
    icon      = _ms_icon(tool.name)
    icon_cls  = _icon_color(tool.name, tool.is_error)
    label     = _tool_display(tool.name, tool.inputs)
    toggle_id = f"tool-{id(tool)}"

    # Build collapsible detail
    detail = ""
    if "edit" in n:
        detail = _render_edit_diff(tool.inputs)
    elif "write" in n:
        detail = _render_write_content(tool.inputs)
    elif "bash" in n and not tool.is_error:
        detail = _render_bash_detail(tool.inputs, tool.result or "")
    elif tool.result and "read" not in n and "glob" not in n and "grep" not in n and not tool.is_error:
        detail = _render_generic_result(tool.result)

    detail_html = (
        f'<div class="tool-detail visible" id="{toggle_id}">{detail}</div>'
        if detail else ""
    )
    toggle_btn = (
        f'<button class="tool-toggle-btn open text-outline text-lg leading-none '
        f'hover:text-on-surface px-1" onclick="toggleDetail(\'{toggle_id}\')" title="Toggle">▾</button>'
        if detail else ""
    )

    if tool.is_error:
        error_body = ""
        if tool.result:
            trunc = tool.result[:800] + ("…" if len(tool.result) > 800 else "")
            error_body = (
                f'<div class="mx-4 mb-3 mt-2 p-4 bg-surface-container-lowest rounded-lg '
                f'border border-error/10">'
                f'<pre class="mono text-xs text-error whitespace-pre-wrap m-0">'
                f'{html.escape(trunc)}</pre></div>'
                f'<div class="px-4 pb-4">'
                f'<div class="flex items-center gap-2 text-xs text-on-surface-variant '
                f'bg-surface-container px-3 py-2 rounded-lg">'
                f'<span class="material-symbols-outlined text-sm">info</span>'
                f'<span>Command failed. Check the output above.</span>'
                f'</div></div>'
            )
        return (
            f'<div class="tool-card mb-4 overflow-hidden rounded-xl '
            f'bg-error-container/5 border-2 border-error/20">\n'
            f'  <div class="flex items-center justify-between px-4 py-3 bg-error-container/10">\n'
            f'    <div class="flex items-center gap-2">\n'
            f'      <span class="material-symbols-outlined text-error text-lg">error</span>\n'
            f'      <span class="text-sm font-semibold mono text-error">{label}</span>\n'
            f'    </div>\n'
            f'    {toggle_btn}\n'
            f'  </div>\n'
            f'  {error_body}\n'
            f'  {detail_html}\n'
            f'</div>'
        )

    badge = (
        '<span class="text-[10px] font-bold text-outline-variant bg-surface-container '
        'px-2 py-0.5 rounded uppercase tracking-wide">Done</span>'
    )
    return (
        f'<div class="tool-card mb-4 overflow-hidden rounded-xl bg-surface-container-low">\n'
        f'  <div class="flex items-center justify-between px-4 py-3 bg-surface-container-high/50">\n'
        f'    <div class="flex items-center gap-2">\n'
        f'      <span class="material-symbols-outlined {icon_cls} text-lg">{icon}</span>\n'
        f'      <span class="text-sm font-semibold mono">{label}</span>\n'
        f'    </div>\n'
        f'    <div class="flex items-center gap-2">\n'
        f'      {badge}\n'
        f'      {toggle_btn}\n'
        f'    </div>\n'
        f'  </div>\n'
        f'  {detail_html}\n'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Full rich turn rendering
# ---------------------------------------------------------------------------

def to_rich_html_body(turns: list, session_id: str = "") -> str:
    """Render a list of RichTurn objects to an HTML fragment."""
    sections: list[str] = []

    # Header
    now = datetime.now().strftime("%b %d, %Y · %I:%M %p")
    session_line = (
        f'<p class="text-sm text-on-surface-variant mt-1 font-medium">'
        f'Session ID: <span class="mono">{html.escape(session_id)}</span></p>'
        if session_id else ""
    )
    sections.append(
        '<div class="mb-12 border-b border-surface-container-high pb-6">\n'
        '  <div class="flex justify-between items-end">\n'
        '    <div>\n'
        '      <h2 class="text-2xl font-extrabold tracking-tight text-on-surface">'
        'Claude Code Response</h2>\n'
        f'      {session_line}\n'
        '    </div>\n'
        f'    <div class="text-right">\n'
        f'      <span class="text-xs uppercase tracking-widest text-outline font-bold">{now}</span>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>'
    )

    for i, turn in enumerate(turns):
        if i > 0:
            sections.append(
                '<div class="relative flex items-center justify-center my-16">\n'
                '  <div class="absolute inset-0 flex items-center">\n'
                '    <div class="w-full border-t-2 border-dashed border-surface-container-high"></div>\n'
                '  </div>\n'
                '  <div class="relative bg-surface px-6">\n'
                '    <span class="material-symbols-outlined text-outline text-xl">auto_awesome</span>\n'
                '  </div>\n'
                '</div>'
            )

        if turn.texts:
            blocks = [
                f'<div class="response-block">{to_html_body(blk)}</div>'
                for blk in turn.texts
                if blk.strip()
            ]
            if blocks:
                sections.append(
                    f'<div class="response-text mb-10 space-y-2">{"".join(blocks)}</div>'
                )

        if turn.tools:
            tool_items = "\n".join(_render_tool_event(t) for t in turn.tools)
            sections.append(f'<div class="mb-8">{tool_items}</div>')

    return "\n".join(sections)
