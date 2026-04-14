---
description: "Preview or export the last response as PDF, DOCX, HTML, or rendered browser preview. Zero tokens consumed — runs locally."
---

# /preview

Export the last assistant response. Runs entirely on your machine — no API calls, no tokens.

## Usage

```
/preview              → open in browser
/preview pdf          → export as PDF
/preview docx         → export as Word document
/preview html         → save as HTML file
/preview md           → save as Markdown file
/preview 3            → last 3 responses in browser
/preview 3 pdf        → last 3 responses as PDF
```

## Process

### 1. Parse arguments

- No args → browser preview
- Format keyword (`pdf`, `docx`, `html`, `md`) → that format
- Leading number → capture last N assistant messages

### 2. Capture content

Collect the most recent assistant message(s) before this command was invoked. Strip all tool call metadata — only include visible text content.

### 3. Write temp input

Write captured content to `/tmp/md-preview-input.md`.

### 4. Convert

Run `md-preview` CLI:

```bash
# browser (default)
md-preview /tmp/md-preview-input.md

# export formats
md-preview /tmp/md-preview-input.md -f pdf -o /tmp/claude-preview.pdf
md-preview /tmp/md-preview-input.md -f docx -o /tmp/claude-preview.docx
md-preview /tmp/md-preview-input.md -f html -o /tmp/claude-preview.html
md-preview /tmp/md-preview-input.md -f md -o /tmp/claude-preview.md
```

### 5. Confirm

One line:

```
preview → /tmp/md-preview.html
```

## Fallback

If `md-preview` is not installed, write a self-contained HTML file directly using the markdown content embedded in a `<script>` tag with marked.js and highlight.js CDN links. Then open with the system browser. Print:

```
md-preview not found — used inline fallback. Install for PDF/DOCX: pip install md-preview
```

## Rules

- Overwrite temp files each time
- Do not ask for confirmation
- Do not interrupt the active task
- Read-only — never modify project files
