"""GitHub-flavored styles for rendering."""

from __future__ import annotations

GITHUB_CSS = """\
:root {
  --color-fg: #1f2328;
  --color-bg: #ffffff;
  --color-border: #d1d9e0;
  --color-subtle: #f6f8fa;
  --color-muted: #656d76;
  --color-link: #0969da;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-fg: #e6edf3;
    --color-bg: #0d1117;
    --color-border: #30363d;
    --color-subtle: #161b22;
    --color-muted: #8b949e;
    --color-link: #58a6ff;
  }
}

@page {
  size: Letter;
  margin: 1in;
  @bottom-right {
    content: "Page " counter(page);
    font: 8pt -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
    color: var(--color-muted);
  }
}

*, *::before, *::after { box-sizing: border-box; }

body {
  font: 16px/1.6 -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  color: var(--color-fg);
  background: var(--color-bg);
  max-width: 860px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 600;
  line-height: 1.25;
  margin: 1.5em 0 0.5em;
  page-break-after: avoid;
}
h1 { font-size: 2em; border-bottom: 1px solid var(--color-border); padding-bottom: .3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid var(--color-border); padding-bottom: .3em; }
h3 { font-size: 1.25em; }

p { margin: 0 0 1em; orphans: 3; widows: 3; }
a { color: var(--color-link); text-decoration: none; }
a:hover { text-decoration: underline; }
strong { font-weight: 600; }

code {
  font: .85em/1 ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace;
  background: var(--color-subtle);
  padding: .2em .4em;
  border-radius: 6px;
}
pre {
  background: var(--color-subtle);
  padding: 1em;
  border-radius: 6px;
  overflow-x: auto;
  margin: 0 0 1em;
  page-break-inside: avoid;
}
pre code { background: none; padding: 0; }

blockquote {
  border-left: 4px solid var(--color-border);
  color: var(--color-muted);
  padding: .5em 1em;
  margin: 0 0 1em;
}

ul, ol { padding-left: 2em; margin: 0 0 1em; }
li { margin-bottom: .25em; }

table { border-collapse: collapse; width: 100%; margin: 0 0 1em; }
th, td { border: 1px solid var(--color-border); padding: .5em 1em; text-align: left; }
th { background: var(--color-subtle); font-weight: 600; }

hr { border: none; border-top: 1px solid var(--color-border); margin: 1.5em 0; }
img { max-width: 100%; }
"""

HTML_WRAPPER = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css" media="(prefers-color-scheme: light)">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css" media="(prefers-color-scheme: dark)">
<style>{css}</style>
</head>
<body>
{body}
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
</body>
</html>"""
