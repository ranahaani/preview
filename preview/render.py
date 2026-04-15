"""Markdown + rich turn rendering."""

from __future__ import annotations

import html
import re
from pathlib import Path

import markdown as md
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import BashLexer, TextLexer, get_lexer_for_filename, guess_lexer
from pygments.util import ClassNotFound


# ---------------------------------------------------------------------------
# Pygments helpers — GitHub light theme for file content, Monokai for bash
# ---------------------------------------------------------------------------

_GITHUB_FMT = HtmlFormatter(style="github-dark", nowrap=True)
_BASH_FMT    = HtmlFormatter(style="monokai",     nowrap=True)


def _highlight_code(code: str, filename: str = "", lang: str = "") -> str:
    """Return syntax-highlighted HTML span sequence (no wrapper div)."""
    try:
        if lang:
            from pygments.lexers import get_lexer_by_name
            lexer = get_lexer_by_name(lang)
        elif filename:
            lexer = get_lexer_for_filename(filename)
        else:
            lexer = guess_lexer(code)
    except ClassNotFound:
        lexer = TextLexer()
    return highlight(code, lexer, _GITHUB_FMT)


def _highlight_bash(cmd: str) -> str:
    return highlight(cmd, BashLexer(), _BASH_FMT)


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def to_html_body(text: str) -> str:
    """Convert raw Markdown text to an HTML fragment."""
    text = re.sub(r"- \[x\]", "- ☑", text)
    text = re.sub(r"- \[ \]", "- ☐", text)
    converter = md.Markdown(
        extensions=["tables", "fenced_code", "codehilite", "nl2br", "sane_lists", "toc"],
        extension_configs={"codehilite": {"css_class": "highlight", "guess_lang": True, "use_pygments": True}},
    )
    return converter.convert(text)


def extract_title(text: str) -> str:
    match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    return match.group(1).strip() if match else "Claude Response"


# ---------------------------------------------------------------------------
# Tool event rendering
# ---------------------------------------------------------------------------

def _tool_icon(name: str) -> str:
    n = name.lower()
    if "edit" in n:   return "✏️"
    if "write" in n:  return "📝"
    if "read" in n:   return "📖"
    if "bash" in n:   return "▶"
    if "glob" in n:   return "🔍"
    if "grep" in n:   return "🔎"
    if "agent" in n:  return "🤖"
    if "web" in n:    return "🌐"
    return "🔧"


def _tool_label(name: str, inputs: dict) -> str:
    n = name.lower()
    path = inputs.get("file_path") or inputs.get("path") or ""
    if "edit" in n:
        return f"Edited <code class='tool-path'>{html.escape(path)}</code>"
    if "write" in n:
        return f"Created <code class='tool-path'>{html.escape(path)}</code>"
    if "read" in n:
        return f"Read <code class='tool-path'>{html.escape(path)}</code>"
    if "bash" in n:
        desc = inputs.get("description", "")
        cmd  = inputs.get("command", "")
        label = html.escape(desc or cmd[:80])
        return f"Ran <code class='tool-cmd'>{label}</code>"
    if "glob" in n:
        return f"Glob <code class='tool-cmd'>{html.escape(inputs.get('pattern', ''))}</code>"
    if "grep" in n:
        return f"Grep <code class='tool-cmd'>{html.escape(inputs.get('pattern', ''))}</code>"
    return html.escape(name)


def _render_highlighted_block(code: str, filename: str = "", css_class: str = "tool-file-content") -> str:
    truncated = code[:3000] + ("\n… (truncated)" if len(code) > 3000 else "")
    highlighted = _highlight_code(truncated, filename=filename)
    return f'<div class="{css_class}"><pre class="gh-highlight">{highlighted}</pre></div>'


def _render_edit_diff(inputs: dict) -> str:
    old = inputs.get("old_string", "")
    new = inputs.get("new_string", "")
    path = inputs.get("file_path", "")
    if not old and not new:
        return ""

    def _hl(code: str) -> str:
        try:
            return _highlight_code(code, filename=path)
        except Exception:
            return html.escape(code)

    out = ['<div class="diff-block">']
    if old:
        out.append(f'<div class="diff-removed"><span class="diff-sign">−</span><pre class="gh-highlight">{_hl(old)}</pre></div>')
    if new:
        out.append(f'<div class="diff-added"><span class="diff-sign">+</span><pre class="gh-highlight">{_hl(new)}</pre></div>')
    out.append("</div>")
    return "\n".join(out)


def _render_write_content(inputs: dict) -> str:
    content = inputs.get("content", "")
    path    = inputs.get("file_path", "")
    if not content:
        return ""
    return _render_highlighted_block(content, filename=path)


def _render_bash_detail(inputs: dict, result: str) -> str:
    cmd = inputs.get("command", "")
    parts = []
    if cmd:
        highlighted = _highlight_bash(cmd)
        safe_cmd = html.escape(cmd, quote=True)
        parts.append(
            f'<div class="bash-command">'
            f'<pre class="bash-pre">{highlighted}</pre>'
            f'<button class="copy-btn" data-copy="{safe_cmd}" title="Copy">Copy</button>'
            f'</div>'
        )
    if result:
        truncated = result[:3000] + ("\n… (truncated)" if len(result) > 3000 else "")
        parts.append(f'<div class="bash-output"><pre><code>{html.escape(truncated)}</code></pre></div>')
    return "\n".join(parts)


def _render_tool_event(tool) -> str:
    n = tool.name.lower()
    icon  = _tool_icon(tool.name)
    label = _tool_label(tool.name, tool.inputs)
    error_cls = " tool-error" if tool.is_error else ""

    detail = ""
    if "edit" in n:
        detail = _render_edit_diff(tool.inputs)
    elif "write" in n:
        detail = _render_write_content(tool.inputs)
    elif "bash" in n:
        detail = _render_bash_detail(tool.inputs, tool.result)
    elif tool.result and "read" not in n:
        trunc = tool.result[:1000] + ("…" if len(tool.result) > 1000 else "")
        detail = f'<div class="tool-result-text"><pre>{html.escape(trunc)}</pre></div>'

    toggle_id  = f"tool-{id(tool)}"
    detail_html = f'<div class="tool-detail" id="{toggle_id}">{detail}</div>' if detail else ""
    toggle_btn  = (
        f'<button class="tool-toggle" onclick="toggleDetail(\'{toggle_id}\')" title="Toggle">▾</button>'
        if detail else ""
    )

    return f"""<div class="tool-event{error_cls}">
  <div class="tool-header">
    <span class="tool-icon">{icon}</span>
    <span class="tool-label">{label}</span>
    {toggle_btn}
  </div>
  {detail_html}
</div>"""


# ---------------------------------------------------------------------------
# Full rich turn rendering
# ---------------------------------------------------------------------------

def to_rich_html_body(turns: list) -> str:
    """Render a list of RichTurn objects to an HTML fragment."""
    sections: list[str] = []

    for i, turn in enumerate(turns):
        parts: list[str] = []

        if turn.texts:
            md_text = "\n\n".join(turn.texts)
            parts.append(f'<div class="response-text">{to_html_body(md_text)}</div>')

        if turn.tools:
            tool_items = "\n".join(_render_tool_event(t) for t in turn.tools)
            parts.append(f'<div class="tool-list">{tool_items}</div>')

        if parts:
            sep = '<hr class="turn-sep">' if i > 0 else ""
            sections.append(f'{sep}<div class="turn">' + "\n".join(parts) + "</div>")

    return "\n".join(sections)
