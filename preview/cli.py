"""CLI entry point."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from preview import __version__
from preview.export import FORMATS, preview_in_browser


def _open_file(path: Path) -> None:
    """Open a file with the OS default application."""
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["open", str(path)], check=False)
    elif system == "Windows":
        subprocess.run(["start", "", str(path)], shell=True, check=False)  # noqa: S602
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


def _check() -> int:
    """Verify all dependencies are installed. Returns exit code."""
    deps = [
        ("markdown", "markdown"),
        ("weasyprint", "weasyprint"),
        ("docx", "python-docx"),
    ]
    missing = []
    for module, package in deps:
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"missing: {', '.join(missing)}")
        print(f"fix:     pip install {' '.join(missing)}")
        return 1

    print("all dependencies installed ✓")
    return 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="preview",
        description="Preview and export Markdown as PDF, DOCX, HTML, or browser preview.",
    )
    parser.add_argument("input", type=Path, help="Markdown file to process")
    parser.add_argument(
        "-f", "--format",
        choices=["pdf", "docx", "html", "md", "preview"],
        default="preview",
        metavar="FORMAT",
        help="output format: pdf, docx, html, md, preview (default: preview)",
    )
    parser.add_argument("-o", "--output", type=Path, help="output file path")
    parser.add_argument("--check", action="store_true", help="verify dependencies and exit")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args(argv)

    if args.check:
        sys.exit(_check())

    src: Path = args.input.expanduser().resolve()
    if not src.is_file():
        sys.exit(f"error: {src} not found")

    text = src.read_text(encoding="utf-8")

    if args.format == "preview":
        path = preview_in_browser(text)
        print(f"preview → {path}")
        return

    fmt = args.format
    output = (args.output or src.with_suffix(f".{fmt}")).expanduser().resolve()
    FORMATS[fmt](text, output)
    print(f"{fmt} → {output}")

    if fmt in ("pdf", "docx"):
        _open_file(output)


if __name__ == "__main__":
    main()
