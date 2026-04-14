<p align="center">
  <h1 align="center">md-preview</h1>
  <p align="center">
    <strong>Preview and export Claude Code responses as PDF, DOCX, or HTML.</strong><br>
    Zero tokens consumed. Runs entirely on your machine.
  </p>
</p>

<p align="center">
  <a href="https://github.com/ranahaani/md-preview/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+"></a>
  <a href="#install"><img src="https://img.shields.io/badge/tokens-zero-brightgreen.svg" alt="Zero Tokens"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg" alt="Cross-platform"></a>
</p>

<p align="center">
  <a href="#install">Install</a> · <a href="#usage">Usage</a> · <a href="#formats">Formats</a> · <a href="#standalone-cli">CLI</a>
</p>

---

## Why

Claude Code outputs Markdown in the terminal. That works for quick answers, but falls apart when you need to:

- **Share** a response with someone who doesn't use the terminal
- **Read** a long response with tables, code blocks, and nested lists
- **Archive** a solution as a properly formatted document
- **Present** Claude's analysis in a meeting

`/preview` fixes this. One command, any format, no tokens burned.

```
You:     Explain the authentication flow in this codebase
Claude:  [long detailed response with code blocks and diagrams]

You:     /preview pdf
Claude:  pdf → /tmp/claude-preview.pdf
```

The PDF opens automatically. Done.

---

## Install

One command:

```bash
curl -fsSL https://raw.githubusercontent.com/ranahaani/md-preview/main/install.sh | bash
```

This installs the `md-preview` CLI and the `/preview` slash command for Claude Code.

<details>
<summary><strong>Manual install</strong></summary>

```bash
# 1. Install the CLI
pip install git+https://github.com/ranahaani/md-preview.git

# 2. Add the slash command
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/preview.md \
  https://raw.githubusercontent.com/ranahaani/md-preview/main/commands/preview.md

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
| Windows | WeasyPrint bundles GTK on recent versions — `pip install weasyprint` is usually enough |

</details>

**Verify:**

```bash
md-preview --check README.md
# all dependencies installed ✓
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
| `/preview md` | Save as Markdown file |
| `/preview 3` | Last 3 responses in browser |
| `/preview 3 pdf` | Last 3 responses as PDF |

**No tokens are consumed.** The command captures the response text that's already in your session and converts it locally.

---

## Formats

| | Browser | PDF | DOCX | HTML |
|---|:---:|:---:|:---:|:---:|
| Headings | ✓ | ✓ | ✓ | ✓ |
| Bold / Italic / Code | ✓ | ✓ | ✓ | ✓ |
| Fenced code blocks | ✓ | ✓ | ✓ | ✓ |
| Tables | ✓ | ✓ | — | ✓ |
| Blockquotes | ✓ | ✓ | ✓ | ✓ |
| Lists | ✓ | ✓ | ✓ | ✓ |
| Checkboxes | ✓ | ✓ | ✓ | ✓ |
| Links / Images | ✓ | ✓ | — | ✓ |
| Syntax highlighting | ✓ | — | — | ✓ |
| Dark mode | ✓ | — | — | ✓ |

---

## Standalone CLI

Works with any Markdown file, independent of Claude Code:

```bash
md-preview README.md                              # browser preview
md-preview README.md -f pdf                        # PDF
md-preview README.md -f docx                       # DOCX
md-preview README.md -f html                       # HTML
md-preview notes.md -f pdf -o ~/Desktop/notes.pdf  # custom output path
```

---

## How it works

```
Claude Code response (already in your terminal — no new API call)
     │
     ▼
 /preview [format]
     │
     ▼
 md-preview CLI (local, offline)
     │
     ├── preview  → temp HTML → default browser
     ├── pdf      → WeasyPrint → paginated PDF
     ├── docx     → python-docx → Word document
     └── html     → highlight.js + GitHub CSS → standalone file
```

The `/preview` command writes the response text to a temp file and calls `md-preview` for conversion. Everything runs on your machine. Nothing is sent anywhere.

---

## Uninstall

```bash
pip uninstall md-preview
rm ~/.claude/commands/preview.md
```

---

## License

MIT — use it however you want.
