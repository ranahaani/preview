"""Professional document styles — ported from generate_pdf.py."""

from __future__ import annotations

from pygments.formatters import HtmlFormatter

_PYGMENTS_CSS      = HtmlFormatter(style="monokai").get_style_defs(".highlight")
_GH_DARK_NOWRAP    = HtmlFormatter(style="friendly",    nowrap=True).get_style_defs(".gh-highlight")
_MONOKAI_NOWRAP    = HtmlFormatter(style="friendly",    nowrap=True).get_style_defs(".bash-pre")

# ---------------------------------------------------------------------------
# Full CSS — Georgia serif body, blue headings, Monokai dark code blocks
# ---------------------------------------------------------------------------
DOCUMENT_CSS = f"""\
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

@page {{
  size: Letter;
  margin: 1.0in 0.95in 0.9in 0.95in;
  @bottom-right {{
    content: "Page " counter(page) " of " counter(pages);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 7.5pt;
    color: #888;
  }}
}}

body {{
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 10pt;
  line-height: 1.65;
  color: #1a1a1a;
  background: #ffffff;
}}

h1, h2, h3, h4 {{
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-weight: 700;
  color: #0d1b2a;
  line-height: 1.25;
  orphans: 3;
  widows: 3;
}}

h1 {{
  font-size: 22pt;
  font-weight: 800;
  color: #0d1b2a;
  margin-top: 0;
  margin-bottom: 6pt;
  padding-bottom: 8pt;
  border-bottom: 2.5pt solid #2563EB;
}}

h2 {{
  font-size: 12.5pt;
  color: #2563EB;
  margin-top: 22pt;
  margin-bottom: 7pt;
  padding-bottom: 3pt;
  border-bottom: 0.75pt solid #93c5fd;
  page-break-after: avoid;
}}

h3 {{
  font-size: 10.5pt;
  color: #1e40af;
  margin-top: 14pt;
  margin-bottom: 5pt;
  page-break-after: avoid;
}}

h4 {{
  font-size: 9.5pt;
  color: #374151;
  margin-top: 10pt;
  margin-bottom: 4pt;
  page-break-after: avoid;
}}

hr {{
  border: none;
  border-top: 0.75pt solid #93c5fd;
  margin: 16pt 0;
}}

p {{
  margin-bottom: 8pt;
  orphans: 3;
  widows: 3;
}}

strong {{ font-weight: 700; color: #0d1b2a; }}
em     {{ font-style: italic; color: #555; }}
a      {{ color: #2563EB; text-decoration: none; }}

ul, ol {{
  margin: 4pt 0 8pt 18pt;
  padding: 0;
}}
ul {{ list-style-type: disc; }}
ol {{ list-style-type: decimal; }}
li {{
  margin-bottom: 4pt;
  orphans: 2;
  widows: 2;
}}
li > ul, li > ol {{ margin-top: 2pt; margin-bottom: 2pt; }}

table {{
  width: 100%;
  border-collapse: collapse;
  margin: 8pt 0 12pt;
  font-size: 9pt;
  page-break-inside: auto;
}}
thead {{
  background: #1e3a5f;
  color: #ffffff;
}}
thead th {{
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 8pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.4pt;
  padding: 6pt 8pt;
  text-align: left;
  border: 0.5pt solid #0d1b2a;
}}
tbody tr:nth-child(even) {{ background: #eff6ff; }}
tbody tr:nth-child(odd)  {{ background: #ffffff; }}
tbody td {{
  padding: 5pt 8pt;
  border: 0.5pt solid #bfdbfe;
  vertical-align: top;
  line-height: 1.45;
  color: #1f2937;
}}
tbody tr:last-child td {{ border-bottom: 1pt solid #2563EB; }}

blockquote {{
  border-left: 3pt solid #2563EB;
  padding: 6pt 12pt;
  margin: 8pt 0;
  color: #374151;
  font-style: italic;
  background: #eff6ff;
  font-size: 9.5pt;
  line-height: 1.55;
}}

/* Pygments Monokai syntax highlighting */
{_PYGMENTS_CSS}

.highlight {{
  background: #272822 !important;
  border-radius: 3pt;
  padding: 10pt 12pt;
  margin: 8pt 0 10pt;
  font-family: 'Courier New', Consolas, monospace;
  font-size: 8pt;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
  page-break-inside: avoid;
  overflow: hidden;
}}
.highlight pre {{
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  color: #f8f8f2;
  font-family: 'Courier New', Consolas, monospace;
  font-size: 8pt;
  line-height: 1.5;
}}
.highlight code {{
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  color: inherit;
  font-family: 'Courier New', Consolas, monospace;
  font-size: 8pt;
}}

/* Inline code */
code {{
  font-family: 'Courier New', Consolas, monospace;
  font-size: 8.5pt;
  background: #e5edff;
  border: 0.4pt solid #93c5fd;
  border-radius: 2pt;
  padding: 1pt 3pt;
  color: #1e40af;
}}
pre code {{ background: transparent; border: none; padding: 0; color: inherit; }}

pre:not(.highlight) {{
  background: #272822;
  border-radius: 3pt;
  padding: 10pt 12pt;
  margin: 8pt 0 10pt;
  font-family: 'Courier New', Consolas, monospace;
  font-size: 8pt;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
  page-break-inside: avoid;
  color: #f8f8f2;
}}
"""

# ---------------------------------------------------------------------------
# HTML variant — same design adapted for browser rendering
# ---------------------------------------------------------------------------
BROWSER_CSS = f"""\
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 17px;
  line-height: 1.7;
  color: #1a1a1a;
  background: #f5f5f0;
  -webkit-font-smoothing: antialiased;
}}

.page {{
  max-width: 820px;
  margin: 2.5rem auto;
  background: #ffffff;
  padding: 3rem 3.5rem;
  border-radius: 4px;
  box-shadow: 0 2px 20px rgba(0,0,0,.08);
}}

h1, h2, h3, h4 {{
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-weight: 700;
  color: #0d1b2a;
  line-height: 1.25;
}}

h1 {{
  font-size: 2rem;
  font-weight: 800;
  margin-top: 0;
  margin-bottom: .5rem;
  padding-bottom: .5rem;
  border-bottom: 3px solid #2563EB;
}}

h2 {{
  font-size: 1.25rem;
  color: #2563EB;
  margin-top: 2rem;
  margin-bottom: .5rem;
  padding-bottom: .25rem;
  border-bottom: 1px solid #93c5fd;
}}

h3 {{
  font-size: 1.05rem;
  color: #1e40af;
  margin-top: 1.5rem;
  margin-bottom: .4rem;
}}

h4 {{
  font-size: .95rem;
  color: #374151;
  margin-top: 1rem;
  margin-bottom: .3rem;
}}

hr {{
  border: none;
  border-top: 1px solid #93c5fd;
  margin: 1.5rem 0;
}}

p {{ margin-bottom: .75rem; }}

strong {{ font-weight: 700; color: #0d1b2a; }}
em {{ font-style: italic; color: #555; }}
a {{ color: #2563EB; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

ul, ol {{ margin: .25rem 0 .75rem 1.5rem; padding: 0; }}
ul {{ list-style-type: disc; }}
ol {{ list-style-type: decimal; }}
li {{ margin-bottom: .25rem; }}

table {{
  width: 100%;
  border-collapse: collapse;
  margin: .75rem 0 1rem;
  font-size: .9rem;
}}
thead {{ background: #1e3a5f; color: #fff; }}
thead th {{
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: .8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .3px;
  padding: .5rem .75rem;
  text-align: left;
}}
tbody tr:nth-child(even) {{ background: #eff6ff; }}
tbody td {{
  padding: .4rem .75rem;
  border: 1px solid #bfdbfe;
  vertical-align: top;
  color: #1f2937;
}}

blockquote {{
  border-left: 3px solid #2563EB;
  padding: .5rem 1rem;
  margin: .75rem 0;
  color: #374151;
  font-style: italic;
  background: #eff6ff;
  border-radius: 0 3px 3px 0;
}}

{_PYGMENTS_CSS}
{_GH_DARK_NOWRAP}
{_MONOKAI_NOWRAP}

/* gh-highlight: used inside diff/write/file blocks (light theme) */
.gh-highlight {{
  background: transparent;
  font-family: 'Courier New', Consolas, monospace;
  font-size: .82rem;
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
  padding: 0;
  color: #333;
}}

/* bash-pre: highlighted shell commands (light theme) */
.bash-pre {{
  background: transparent;
  font-family: 'Courier New', Consolas, monospace;
  font-size: .82rem;
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
  padding: 0;
  color: #333;
}}

.highlight {{
  background: #272822 !important;
  border-radius: 6px;
  padding: 1rem 1.25rem;
  margin: .75rem 0 1rem;
  font-family: 'Courier New', Consolas, monospace;
  font-size: .82rem;
  line-height: 1.55;
  overflow-x: auto;
}}
.highlight pre {{
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  color: #f8f8f2;
  font-size: .82rem;
}}
.highlight code {{
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  color: inherit;
  font-size: .82rem;
}}

code {{
  font-family: 'Courier New', Consolas, monospace;
  font-size: .85rem;
  background: #e5edff;
  border: 1px solid #93c5fd;
  border-radius: 3px;
  padding: 1px 5px;
  color: #1e40af;
}}
pre code {{ background: transparent; border: none; padding: 0; color: inherit; }}

pre:not(.highlight) {{
  background: #272822;
  border-radius: 6px;
  padding: 1rem 1.25rem;
  margin: .75rem 0 1rem;
  font-family: 'Courier New', Consolas, monospace;
  font-size: .82rem;
  line-height: 1.55;
  overflow-x: auto;
  color: #f8f8f2;
}}

/* ── Copy buttons on code blocks ── */
.code-wrapper {{
  position: relative;
}}
.copy-btn {{
  position: absolute;
  top: .45rem;
  right: .5rem;
  background: rgba(0,0,0,.06);
  color: #6b7280;
  border: 1px solid rgba(0,0,0,.12);
  border-radius: 4px;
  padding: 4px 5px;
  line-height: 0;
  cursor: pointer;
  transition: background .15s, color .15s;
  z-index: 10;
  display: flex;
  align-items: center;
}}
.copy-btn:hover {{ background: rgba(0,0,0,.12); color: #111; }}
.copy-btn.copied {{ background: #16a34a; color: #fff; border-color: #16a34a; }}

/* ── Tool events ── */
.tool-list {{
  margin: 1.25rem 0 .5rem;
  display: flex;
  flex-direction: column;
  gap: .5rem;
}}

.tool-event {{
  border: 1px solid #e2e8f0;
  border-left: 3px solid #93c5fd;
  border-radius: 0 6px 6px 0;
  background: #f8faff;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: .85rem;
}}

.tool-event.tool-error {{
  border-left-color: #f87171;
  background: #fff5f5;
}}

.tool-header {{
  display: flex;
  align-items: center;
  gap: .5rem;
  padding: .45rem .75rem;
  cursor: default;
}}

.tool-icon {{
  flex-shrink: 0;
  display: flex;
  align-items: center;
  color: #6b7280;
}}

.tool-label {{ flex: 1; color: #374151; }}
.tool-label code.tool-path {{
  font-family: 'Courier New', Consolas, monospace;
  font-size: .8rem;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 3px;
  padding: 1px 5px;
  color: #1d4ed8;
}}
.tool-label code.tool-cmd {{
  font-family: 'Courier New', Consolas, monospace;
  font-size: .8rem;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 3px;
  padding: 1px 5px;
  color: #334155;
}}

.tool-toggle {{
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  font-size: 1rem;
  padding: 0 .25rem;
  line-height: 1;
  transition: transform .2s;
}}
.tool-toggle.open {{ transform: rotate(180deg); }}

.tool-detail {{
  display: none;
  border-top: 1px solid #e2e8f0;
}}
.tool-detail.visible {{ display: block; }}

/* Diff */
.diff-block {{ font-family: 'Courier New', Consolas, monospace; font-size: .78rem; }}
.diff-removed {{
  background: #fef2f2;
  border-top: 1px solid #fecaca;
  padding: .5rem .75rem;
  display: flex;
  gap: .5rem;
}}
.diff-added {{
  background: #f0fdf4;
  border-top: 1px solid #bbf7d0;
  padding: .5rem .75rem;
  display: flex;
  gap: .5rem;
}}
.diff-sign {{
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
  margin-top: .1rem;
  user-select: none;
}}
.diff-removed .diff-sign {{ color: #dc2626; }}
.diff-added  .diff-sign  {{ color: #16a34a; }}
.diff-removed pre.gh-highlight,
.diff-added   pre.gh-highlight {{
  margin: 0; background: transparent; padding: 0; flex: 1;
}}

/* Bash detail */
.bash-command {{
  position: relative;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  padding: .6rem .75rem;
  border-radius: 0;
}}
.bash-command pre.bash-pre {{
  margin: 0; background: transparent; padding: 0;
}}
.bash-command .copy-btn {{
  position: absolute; top: .35rem; right: .5rem;
}}
.bash-output {{
  background: #fafafa;
  border-top: 1px solid #f0f0f0;
  padding: .6rem .75rem;
  max-height: 280px;
  overflow-y: auto;
}}
.bash-output pre {{
  margin: 0; background: transparent; padding: 0;
  color: #374151; font-size: .78rem; line-height: 1.5; white-space: pre-wrap;
}}

/* File content */
.tool-file-content {{
  background: #fafafa;
  border-top: 1px solid #e5e7eb;
  padding: .6rem .75rem;
  max-height: 400px;
  overflow-y: auto;
  border-radius: 0 0 6px 6px;
}}
.tool-file-content pre.gh-highlight {{
  margin: 0; background: transparent; padding: 0;
}}

.tool-result-text {{
  padding: .5rem .75rem;
  background: #f9fafb;
  font-size: .8rem; color: #374151;
}}
.tool-result-text pre {{
  margin: 0; background: transparent; white-space: pre-wrap;
  font-family: 'Courier New', Consolas, monospace; font-size: .78rem;
}}

.turn-sep {{ border: none; border-top: 2px dashed #bfdbfe; margin: 2rem 0; }}

/* Individual text blocks within a turn — slight gap between them */
.response-block {{ margin-bottom: .25rem; }}
.response-block:last-child {{ margin-bottom: 0; }}
"""

COPY_BUTTON_JS = """\
<script>
var _ICON_COPY = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
var _ICON_CHECK = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';

function toggleDetail(id) {
  var el = document.getElementById(id);
  var btn = el.previousElementSibling ? el.parentElement.querySelector('.tool-toggle') : null;
  if (el.classList.contains('visible')) {
    el.classList.remove('visible');
    if (btn) btn.classList.remove('open');
  } else {
    el.classList.add('visible');
    if (btn) btn.classList.add('open');
  }
}

function _flashCopied(btn) {
  btn.innerHTML = _ICON_CHECK;
  btn.classList.add('copied');
  setTimeout(function() { btn.innerHTML = _ICON_COPY; btn.classList.remove('copied'); }, 1800);
}

function attachCopyButtons() {
  // Code blocks
  document.querySelectorAll('pre').forEach(function(pre) {
    if (pre.closest('.bash-command')) return; // already has button
    var wrapper = document.createElement('div');
    wrapper.className = 'code-wrapper';
    wrapper.style.position = 'relative';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);
    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.innerHTML = _ICON_COPY;
    btn.title = 'Copy';
    btn.addEventListener('click', function() {
      var code = pre.querySelector('code') || pre;
      navigator.clipboard.writeText(code.innerText).then(function() { _flashCopied(btn); });
    });
    wrapper.appendChild(btn);
  });

  // Bash command copy buttons (data-copy attr)
  document.querySelectorAll('button[data-copy]').forEach(function(btn) {
    btn.innerHTML = _ICON_COPY;
    btn.title = 'Copy';
    btn.addEventListener('click', function() {
      navigator.clipboard.writeText(btn.dataset.copy).then(function() { _flashCopied(btn); });
    });
  });
}

document.addEventListener('DOMContentLoaded', attachCopyButtons);
</script>"""

HTML_WRAPPER = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="page">
{body}
</div>
{js}
</body>
</html>"""

# Keep old names as aliases so nothing breaks
GITHUB_CSS = BROWSER_CSS
PYGMENTS_CSS = _PYGMENTS_CSS
