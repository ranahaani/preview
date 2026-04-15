---
description: "Preview or export the last assistant response as browser page, PDF, DOCX, HTML, or Markdown."
---

# /preview

Run the `preview` CLI. It reads the last assistant response directly from the Claude Code session files — no manual extraction needed.

## Arguments

`$ARGUMENTS` contains the user's input after `/preview`.

- Empty → open in default browser
- `pdf` → export as PDF
- `docx` → export as Word document
- `html` → save as HTML file
- `md` → save as Markdown file
- Leading number (e.g. `3`, `3 pdf`) → capture last N assistant messages

## Steps

### 1. Parse arguments

Extract optional count (leading number) and format from `$ARGUMENTS`.

### 2. Run the CLI

```bash
# default — last response in browser
preview

# with count
preview -n 3

# with format
preview -f pdf -o /tmp/claude-preview.pdf
preview -f docx -o /tmp/claude-preview.docx
preview -f html -o /tmp/claude-preview.html
preview -f md -o /tmp/claude-preview.md

# count + format
preview -n 3 -f pdf -o /tmp/claude-preview.pdf
```

### 3. Confirm

Print one line with the output path. Nothing else.

## Fallback

If `preview` CLI is not found:
- Print: `preview CLI not found. Install: pip install git+https://github.com/ranahaani/preview.git`

## Rules

- Do NOT ask for confirmation — just do it
- Do NOT explain what you're doing — just output the result line
- Do NOT manually extract conversation content — the CLI reads session files directly
- Never modify project files
