"""Professional document styles — ported from generate_pdf.py."""

from __future__ import annotations

from pygments.formatters import HtmlFormatter

_PYGMENTS_CSS   = HtmlFormatter(style="monokai").get_style_defs(".highlight")
_GH_DARK_NOWRAP = HtmlFormatter(style="friendly", nowrap=True).get_style_defs(".gh-highlight")

# ---------------------------------------------------------------------------
# DOCUMENT_CSS — Georgia serif body, blue headings, Monokai dark code blocks
# (used for PDF export, unchanged)
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
# BROWSER_CSS — minimal overrides; Tailwind handles layout/colour tokens
# ---------------------------------------------------------------------------
BROWSER_CSS = f"""\
body {{ font-family: 'Inter', sans-serif; }}
.mono {{ font-family: 'JetBrains Mono', monospace; }}
.material-symbols-outlined {{
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  user-select: none;
}}

/* Custom scrollbar for terminal blocks */
.terminal-scroll::-webkit-scrollbar {{ width: 6px; height: 6px; }}
.terminal-scroll::-webkit-scrollbar-track {{ background: transparent; }}
.terminal-scroll::-webkit-scrollbar-thumb {{
  background: rgba(113, 124, 130, 0.2);
  border-radius: 10px;
}}

/* ── Markdown content inside .response-text ── */
.response-text p {{ margin-bottom: 0.75rem; line-height: 1.7; color: #2a3439; }}
.response-text h1, .response-text h2, .response-text h3, .response-text h4 {{
  font-weight: 700; color: #2a3439;
  margin-top: 1.5rem; margin-bottom: 0.5rem; line-height: 1.3;
}}
.response-text h1 {{
  font-size: 1.5rem;
  border-bottom: 1px solid #e1e9ee;
  padding-bottom: 0.5rem;
}}
.response-text h2 {{ font-size: 1.25rem; color: #005ac2; }}
.response-text h3 {{ font-size: 1.05rem; color: #004fab; }}
.response-text code {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  background: #e8eff3;
  border-radius: 4px;
  padding: 1px 6px;
  color: #005ac2;
}}
.response-text pre {{
  background: #0b0f10;
  border-radius: 8px;
  padding: 1rem 1.25rem;
  overflow-x: auto;
  margin: 0.75rem 0;
}}
.response-text pre code {{
  background: transparent;
  color: #f8f8f2;
  padding: 0;
  font-size: 0.82rem;
}}
.response-text ul, .response-text ol {{ margin: 0.5rem 0 0.75rem 1.5rem; }}
.response-text li {{ margin-bottom: 0.25rem; }}
.response-text blockquote {{
  border-left: 3px solid #005ac2;
  padding: 0.5rem 1rem;
  background: #f0f4f7;
  margin: 0.75rem 0;
  color: #566166;
  font-style: italic;
  border-radius: 0 4px 4px 0;
}}
.response-text a {{ color: #005ac2; text-decoration: underline; }}
.response-text strong {{ font-weight: 700; color: #2a3439; }}
.response-text em {{ font-style: italic; color: #566166; }}
.response-text table {{
  width: 100%; border-collapse: collapse;
  margin: 0.75rem 0; font-size: 0.9rem;
}}
.response-text thead {{ background: #005ac2; color: white; }}
.response-text th, .response-text td {{
  padding: 0.5rem 0.75rem; border: 1px solid #e1e9ee;
}}
.response-text tbody tr:nth-child(even) {{ background: #f0f4f7; }}
.response-text hr {{
  border: none; border-top: 1px solid #e1e9ee; margin: 1.5rem 0;
}}

/* ── Tool detail toggle ── */
.tool-detail {{ display: none; }}
.tool-detail.visible {{ display: block; }}
.tool-toggle-btn {{ transition: transform 0.2s; }}
.tool-toggle-btn.open {{ transform: rotate(180deg); }}

/* ── Copy buttons ── */
.code-wrapper {{ position: relative; }}
.copy-btn {{
  position: absolute; top: 0.45rem; right: 0.5rem;
  background: rgba(0,0,0,.06); color: #6b7280;
  border: 1px solid rgba(0,0,0,.12); border-radius: 4px;
  padding: 4px 5px; line-height: 0; cursor: pointer;
  transition: background .15s, color .15s; z-index: 10;
  display: flex; align-items: center;
}}
.copy-btn:hover {{ background: rgba(0,0,0,.12); color: #111; }}
.copy-btn.copied {{ background: #16a34a; color: #fff; border-color: #16a34a; }}

/* ── Pygments in write/read file blocks ── */
{_GH_DARK_NOWRAP}
.gh-highlight {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem; line-height: 1.55;
  white-space: pre-wrap; word-break: break-all; color: #333;
}}
"""

# ---------------------------------------------------------------------------
# JS — toggle + copy buttons
# ---------------------------------------------------------------------------
COPY_BUTTON_JS = """\
<script>
var _ICON_COPY = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
var _ICON_CHECK = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';

function toggleDetail(id) {
  var el = document.getElementById(id);
  if (!el) return;
  var btn = el.closest('.tool-card') && el.closest('.tool-card').querySelector('.tool-toggle-btn');
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
  document.querySelectorAll('pre').forEach(function(pre) {
    if (pre.closest('.bash-command')) return;
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

# ---------------------------------------------------------------------------
# HTML wrapper — Tailwind CDN + Google Fonts + Material Symbols
# ---------------------------------------------------------------------------
HTML_WRAPPER = """\
<!DOCTYPE html>
<html class="light" lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<script id="tailwind-config">
tailwind.config = {{
  darkMode: "class",
  theme: {{
    extend: {{
      colors: {{
        "tertiary": "#006d4a",
        "surface-container-highest": "#d9e4ea",
        "surface-dim": "#cfdce3",
        "secondary-fixed-dim": "#c7d5ed",
        "surface-container-low": "#f0f4f7",
        "on-tertiary-fixed-variant": "#006544",
        "surface-container-high": "#e1e9ee",
        "primary-dim": "#004fab",
        "outline": "#717c82",
        "inverse-primary": "#4d8eff",
        "on-primary-fixed": "#003c86",
        "primary": "#005ac2",
        "on-tertiary-container": "#005a3c",
        "secondary": "#526074",
        "error": "#9f403d",
        "surface-variant": "#d9e4ea",
        "on-secondary-fixed": "#324053",
        "inverse-surface": "#0b0f10",
        "on-surface": "#2a3439",
        "surface-bright": "#f7f9fb",
        "secondary-container": "#d5e3fc",
        "on-background": "#2a3439",
        "secondary-dim": "#465468",
        "tertiary-fixed-dim": "#58e7ab",
        "background": "#f7f9fb",
        "tertiary-dim": "#005f40",
        "on-primary": "#f7f7ff",
        "surface-tint": "#005ac2",
        "on-surface-variant": "#566166",
        "tertiary-fixed": "#69f6b8",
        "tertiary-container": "#69f6b8",
        "on-secondary-container": "#455367",
        "surface": "#f7f9fb",
        "surface-container-lowest": "#ffffff",
        "error-dim": "#4e0309",
        "on-primary-fixed-variant": "#0057bd",
        "surface-container": "#e8eff3",
        "primary-fixed": "#d8e2ff",
        "outline-variant": "#a9b4b9",
        "on-primary-container": "#004eaa",
        "on-secondary": "#f8f8ff",
        "error-container": "#fe8983",
        "on-error-container": "#752121",
        "on-error": "#fff7f6",
        "on-tertiary": "#e6ffee",
        "primary-fixed-dim": "#c3d4ff",
        "primary-container": "#d8e2ff",
        "on-tertiary-fixed": "#00452d",
        "on-secondary-fixed-variant": "#4e5c71",
        "inverse-on-surface": "#9a9d9f",
        "secondary-fixed": "#d5e3fc"
      }},
      borderRadius: {{
        "DEFAULT": "0.125rem",
        "lg": "0.25rem",
        "xl": "0.5rem",
        "full": "0.75rem"
      }},
      fontFamily: {{
        headline: ["Inter", "sans-serif"],
        body: ["Inter", "sans-serif"],
        label: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"]
      }}
    }}
  }}
}}
</script>
<style>
{css}
</style>
</head>
<body class="bg-surface text-on-surface antialiased">
<main class="pt-12 pb-20 px-6 sm:px-12 flex justify-center">
<div class="max-w-[800px] w-full">
{body}
</div>
</main>
{js}
</body>
</html>"""

# Keep old names as aliases so nothing breaks
GITHUB_CSS  = BROWSER_CSS
PYGMENTS_CSS = _PYGMENTS_CSS
