#!/usr/bin/env python3
"""Check exact evidence tokens across an editorial revision."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
from pathlib import Path

SCHEMA_VERSION = "agent-plus-editorial-preservation/v1"

TOKEN_PATTERNS = (
    re.compile(r"https?://[^\s)>\]}]+"),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"(?<![\w.])(?:[$£€])?\d[\d,]*(?:\.\d+)?(?:%|[A-Za-z]+)?(?![\w.])"),
    re.compile(r"\[[^\]\n]+\]\(https?://[^)\n]+\)"),
    re.compile(r'"[^"\n]+"'),
    re.compile(r"“[^”\n]+”"),
)


def extract_tokens(text: str, protected: Iterable[str]) -> list[str]:
    """Return unique evidence tokens in stable source order."""
    found: list[tuple[int, str]] = []
    for pattern in TOKEN_PATTERNS:
        found.extend((match.start(), match.group(0)) for match in pattern.finditer(text))
    for value in protected:
        if not value:
            raise ValueError("Protected terms must not be empty")
        start = text.find(value)
        if start < 0:
            raise ValueError(f"Protected term is absent from source: {value}")
        found.append((start, value))

    unique: list[str] = []
    seen: set[str] = set()
    for _, token in sorted(found, key=lambda item: (item[0], -len(item[1]), item[1])):
        if token not in seen:
            seen.add(token)
            unique.append(token)
    return unique


def build_receipt(source: str, revised: str, protected: Iterable[str]) -> dict[str, object]:
    tokens = extract_tokens(source, protected)
    missing = [token for token in tokens if token not in revised]
    return {
        "schema_version": SCHEMA_VERSION,
        "verdict": "PASS" if not missing else "BLOCK",
        "checked_tokens": len(tokens),
        "missing_tokens": missing,
        "limits": [
            "Exact-token preservation only",
            "Does not verify semantic equivalence, causality, uncertainty, or voice",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--protect", action="append", default=[])
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        receipt = build_receipt(
            args.source.read_text(encoding="utf-8"),
            args.revised.read_text(encoding="utf-8"),
            args.protect,
        )
    except (OSError, UnicodeError, ValueError) as exc:
        receipt = {
            "schema_version": SCHEMA_VERSION,
            "verdict": "BLOCK",
            "error": str(exc),
        }

    if args.format == "json":
        print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    elif receipt["verdict"] == "PASS":
        print(f"PASS: preserved {receipt['checked_tokens']} exact evidence tokens")
    else:
        print(f"BLOCK: {receipt.get('error') or receipt.get('missing_tokens')}")
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
