<p align="center">
  <h1 align="center">/preview</h1>
  <p align="center">
    <strong>A Claude Code slash command that renders your last response as a beautiful document.</strong><br>
    Shows assistant text, file changes, tool calls, and bash output — with one-click copy buttons.
  </p>
</p>

<p align="center">
  <a href="https://github.com/ranahaani/preview/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg" alt="Cross-platform"></a>
</p>

<p align="center">
  <a href="#install">Install</a> · <a href="#usage">Usage</a> · <a href="#what-gets-rendered">What gets rendered</a> · <a href="#formats">Formats</a> · <a href="#standalone-cli">CLI</a>
</p>

---

## Why

Claude Code outputs raw text in the terminal. That's fine for quick answers, but falls apart when Claude just:

- Edited 5 files and explained the changes
- Ran several commands and showed their output
- Wrote a detailed architecture explanation with code examples

`/preview` opens all of that as a beautiful, readable document — same design language as a professional PDF report.

```
You:     Refactor the auth module to use JWT
Claude:  [edits 4 files, runs tests, explains what changed]

You:     /preview
→ browser opens with full response: text + diffs + bash output + copy buttons

You:     /preview pdf
→ PDF saved and opened automatically
```

---

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/ranahaani/preview/main/install.sh | bash
```

This installs the `preview` CLI and the `/preview` slash command for Claude Code.

<details>
<summary><strong>Manual install</strong></summary>

```bash
# 1. Install the CLI
pip install git+https://github.com/ranahaani/preview.git

# 2. Add the slash command
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/preview.md \
  https://raw.githubusercontent.com/ranahaani/preview/main/commands/preview.md

# 3. Restart Claude Code
```

</details>

<details>
<summary><strong>System dependencies for PDF (WeasyPrint)</strong></summary>

PDF export uses WeasyPrint, which needs system libraries:

| OS | Command |
|---|---|
| macOS | `brew install pango libffi` |
| Ubuntu/Debian | `sudo apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev` |
| Fedora/RHEL | `sudo dnf install pango gdk-pixbuf2 libffi-devel` |
| Windows | `pip install weasyprint` (bundles GTK on recent versions) |

</details>

**Verify:**

```bash
preview --check
# all dependencies installed
```

---

## Usage

Inside any Claude Code session:

| Command | What it does |
|---|---|
| `/preview` | Open last response in browser |
| `/preview pdf` | Export as PDF |
| `/preview docx` | Export as Word document |
| `/preview html` | Save as standalone HTML |
| `/preview md` | Save raw Markdown |
| `/preview 3` | Last 3 responses in browser |
| `/preview 3 pdf` | Last 3 responses as PDF |

Reads directly from Claude Code's session files — no copy-paste needed.

---

## What gets rendered

Each response is rendered as a complete document:

### Assistant text
Markdown rendered with Georgia serif body, blue headings, Monokai dark code blocks.

### Tool events
Every tool call is shown as a collapsible block:

| Tool | What's shown |
|---|---|
| **Edit** | File path + red/green diff of what changed |
| **Write** | File path + file content |
| **Bash** | Command (with copy button) + output |
| **Read** | File path |
| **Glob / Grep** | Pattern used |

### Copy buttons
Every code block and every bash command has a **Copy** button in the top-right corner.

---

## Formats

| | Browser | PDF | DOCX | HTML |
|---|:---:|:---:|:---:|:---:|
| Headings | ✓ | ✓ | ✓ | ✓ |
| Bold / Italic / Code | ✓ | ✓ | ✓ | ✓ |
| Fenced code blocks | ✓ | ✓ | ✓ | ✓ |
| Syntax highlighting (Monokai) | ✓ | ✓ | — | ✓ |
| Copy buttons | ✓ | — | — | ✓ |
| File diffs | ✓ | — | — | ✓ |
| Bash output | ✓ | — | — | ✓ |
| Tables | ✓ | ✓ | — | ✓ |
| Blockquotes | ✓ | ✓ | ✓ | ✓ |
| Page numbers | — | ✓ | — | — |

PDF renders the assistant text only (tool blocks are not print-friendly).

---

## Standalone CLI

Works with any Markdown file, independent of Claude Code:

```bash
preview README.md                              # browser
preview README.md -f pdf                       # PDF
preview README.md -f docx                      # DOCX
preview README.md -f html                      # HTML
preview notes.md -f pdf -o ~/Desktop/notes.pdf # custom path
```

---

## How it works

```
Claude Code session (JSONL files in ~/.claude/projects/)
     │
     ▼
 preview --session (or /preview slash command)
     │
     ├── Reads latest session JSONL
     ├── Groups entries into turns
     │     (tool results don't break turns — one real user msg = one turn)
     ├── Finds last substantive turn (has tool use + text)
     ├── Extracts text blocks + tool calls + results
     │
     ▼
 Rich HTML renderer
     │
     ├── Markdown text → Georgia serif, blue headings
     ├── Edit events → red/green diff blocks
     ├── Bash events → dark command + output panels
     ├── Copy buttons injected on all code/command blocks
     │
     ▼
 preview / pdf / docx / html / md
```

---

## Uninstall

```bash
pip uninstall preview
rm ~/.claude/commands/preview.md
```

---

## License

MIT — use it however you want.
