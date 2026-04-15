#!/usr/bin/env bash
set -euo pipefail

# preview installer
# Usage: curl -fsSL https://raw.githubusercontent.com/ranahaani/preview/main/install.sh | bash

REPO="ranahaani/preview"
BRANCH="main"
RAW="https://raw.githubusercontent.com/${REPO}/${BRANCH}"
COMMANDS_DIR="${HOME}/.claude/commands"

info()  { printf "\033[1;34m→\033[0m %s\n" "$*"; }
ok()    { printf "\033[1;32m✓\033[0m %s\n" "$*"; }
warn()  { printf "\033[1;33m!\033[0m %s\n" "$*"; }
fail()  { printf "\033[1;31m✗\033[0m %s\n" "$*"; exit 1; }

# ── Detect Python ──────────────────────────────────────────────────────────
PYTHON=""
for cmd in python3 python; do
  if command -v "$cmd" &>/dev/null; then
    version=$("$cmd" -c "import sys; print(sys.version_info[:2] >= (3, 10))" 2>/dev/null || echo "False")
    if [ "$version" = "True" ]; then
      PYTHON="$cmd"
      break
    fi
  fi
done
[ -n "$PYTHON" ] || fail "Python 3.10+ required. Install from https://python.org"
ok "Python: $($PYTHON --version)"

# ── Detect pip ─────────────────────────────────────────────────────────────
PIP=""
for cmd in pip3 pip; do
  if command -v "$cmd" &>/dev/null; then
    PIP="$cmd"
    break
  fi
done
[ -n "$PIP" ] || PIP="$PYTHON -m pip"

# ── Install preview package ─────────────────────────────────────────────
info "Installing preview..."
if $PIP install "git+https://github.com/${REPO}.git" --quiet 2>/dev/null; then
  ok "preview installed"
elif $PIP install "git+https://github.com/${REPO}.git" --quiet --user 2>/dev/null; then
  ok "preview installed (user)"
elif $PIP install "git+https://github.com/${REPO}.git" --quiet --break-system-packages 2>/dev/null; then
  ok "preview installed (system)"
else
  fail "pip install failed. Try: pip install git+https://github.com/${REPO}.git"
fi

# ── Install /preview command ──────────────────────────────────────────────
info "Installing /preview command..."
mkdir -p "$COMMANDS_DIR"
curl -fsSL "${RAW}/commands/preview.md" -o "${COMMANDS_DIR}/preview.md"
ok "/preview command → ${COMMANDS_DIR}/preview.md"

# ── Check system deps (WeasyPrint) ────────────────────────────────────────
if ! $PYTHON -c "import weasyprint" 2>/dev/null; then
  warn "WeasyPrint needs system libraries for PDF export:"
  case "$(uname -s)" in
    Darwin)  warn "  brew install pango libffi" ;;
    Linux)   warn "  sudo apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev" ;;
    *)       warn "  See: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html" ;;
  esac
fi

# ── Done ──────────────────────────────────────────────────────────────────
echo ""
ok "Done. Restart Claude Code, then type /preview"
echo ""
echo "   /preview          open last response in browser"
echo "   /preview pdf      export as PDF"
echo "   /preview docx     export as Word document"
echo ""
