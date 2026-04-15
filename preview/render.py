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
# Pygments helpers — friendly light theme for all code blocks
# ---------------------------------------------------------------------------

_GITHUB_FMT = HtmlFormatter(style="friendly", nowrap=True)
_BASH_FMT    = HtmlFormatter(style="friendly", nowrap=True)


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

_SVG = {
    "edit": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>'
        '<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>'
        '</svg>'
    ),
    "write": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/>'
        '</svg>'
    ),
    "read": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>'
        '<circle cx="12" cy="12" r="3"/>'
        '</svg>'
    ),
    "bash": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="4 17 10 11 4 5"/>'
        '<line x1="12" y1="19" x2="20" y2="19"/>'
        '</svg>'
    ),
    "glob": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>'
        '</svg>'
    ),
    "grep": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="11" cy="11" r="8"/>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"/>'
        '</svg>'
    ),
    "agent": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="3" width="18" height="18" rx="2"/>'
        '<circle cx="8.5" cy="10" r="1.5"/><circle cx="15.5" cy="10" r="1.5"/>'
        '<path d="M8 15s1.5 2 4 2 4-2 4-2"/>'
        '</svg>'
    ),
    "web": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="2" y1="12" x2="22" y2="12"/>'
        '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
        '</svg>'
    ),
    "default": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94'
        'l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'
        '</svg>'
    ),
}


def _tool_icon(name: str) -> str:
    n = name.lower()
    if "edit" in n:   return _SVG["edit"]
    if "write" in n:  return _SVG["write"]
    if "read" in n:   return _SVG["read"]
    if "bash" in n:   return _SVG["bash"]
    if "glob" in n:   return _SVG["glob"]
    if "grep" in n:   return _SVG["grep"]
    if "agent" in n:  return _SVG["agent"]
    if "web" in n:    return _SVG["web"]
    return _SVG["default"]


def _tool_label(name: str, inputs: dict) -> str:
    n = name.lower()
    path = inputs.get("file_path") or inputs.get("path") or ""
    if path and ("edit" in n or "write" in n or "read" in n):
        return f"<code class='tool-path'>{html.escape(path)}</code>"
    if "bash" in n:
        desc = inputs.get("description", "")
        cmd  = inputs.get("command", "")
        label = html.escape(desc or cmd[:80])
        return f"<code class='tool-cmd'>{label}</code>"
    if "glob" in n:
        return f"<code class='tool-cmd'>{html.escape(inputs.get('pattern', ''))}</code>"
    if "grep" in n:
        return f"<code class='tool-cmd'>{html.escape(inputs.get('pattern', ''))}</code>"
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
        _copy_icon = (
            '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
            ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="9" y="9" width="13" height="13" rx="2"/>'
            '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>'
            '</svg>'
        )
        parts.append(
            f'<div class="bash-command">'
            f'<pre class="bash-pre">{highlighted}</pre>'
            f'<button class="copy-btn" data-copy="{safe_cmd}" title="Copy">{_copy_icon}</button>'
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
            # Render each text block independently so markdown structure is
            # preserved per block (joining 11 blocks into one string breaks lists).
            blocks = [
                f'<div class="response-block">{to_html_body(blk)}</div>'
                for blk in turn.texts
                if blk.strip()
            ]
            if blocks:
                parts.append(f'<div class="response-text">{"".join(blocks)}</div>')

        if turn.tools:
            tool_items = "\n".join(_render_tool_event(t) for t in turn.tools)
            parts.append(f'<div class="tool-list">{tool_items}</div>')

        if parts:
            sep = '<hr class="turn-sep">' if i > 0 else ""
            sections.append(f'{sep}<div class="turn">' + "\n".join(parts) + "</div>")

    return "\n".join(sections)
