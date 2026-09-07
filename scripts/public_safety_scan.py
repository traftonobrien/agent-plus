#!/usr/bin/env python3
"""Scan the Git publication inventory without printing matched content."""

import re
import subprocess
import sys
from pathlib import Path

PATTERNS = (
    re.compile(r"/" r"Users/"),
    re.compile(r"/" r"Library/Application Support/"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AIza[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
)
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf"}


def scan(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "-z"],
        capture_output=True,
        check=True,
    )
    blocked = []
    for name in sorted(set(result.stdout.decode().split("\0")) - {""}):
        path = root / name
        if path.is_symlink():
            blocked.append(name + ": symlink")
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in BINARY:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            blocked.append(name + ": unsupported binary")
            continue
        if any(pattern.search(text) for pattern in PATTERNS):
            blocked.append(name + ": sensitive pattern (redacted)")
    return blocked


if __name__ == "__main__":
    try:
        findings = scan(Path(__file__).resolve().parents[1])
        for finding in findings:
            print(finding, file=sys.stderr)
        print("PUBLIC_TEXT_SAFETY_" + ("BLOCK" if findings else "PASS"))
        raise SystemExit(bool(findings))
    except (OSError, UnicodeError, subprocess.SubprocessError):
        print("PUBLIC_TEXT_SAFETY_BLOCK inventory unavailable", file=sys.stderr)
        raise SystemExit(1)
