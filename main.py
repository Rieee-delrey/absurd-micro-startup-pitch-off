#!/usr/bin/env python3
"""Absurd Micro-Startup Pitch-Off entry: write the pitch line byte-for-byte.

The entry gate is 1-200 UTF-8 characters, a single line, not only
whitespace. This program validates the line before writing it and
reads the file back to confirm the bytes on disk match exactly.
"""

import hashlib
import os
import sys

ENTRY = "A micro-SaaS that renames your agent's failed tasks as strategic pivots in the status report, one dollar per rebrand, no human ever checks the diff."
EXPECTED_SHA256 = "0849da3fbb4c6f489b3370ce13e8469249ac87f3bb221062f4cb4ac0aada9d6e"
OUTPUT_PATH = "/output/entry.txt"

MIN_CHARS = 1
MAX_CHARS = 200


def main() -> int:
    text = ENTRY
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        print(f"entry is {len(text)} chars, outside the 1-200 gate", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is blank", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if text.count(".") != 1 or not text.endswith("."):
        print("entry must be exactly one sentence", file=sys.stderr)
        return 1

    data = text.encode("utf-8")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)

    # Read-back verification: re-read and check the sha256 hash.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"hash mismatch: got {digest}, expected {EXPECTED_SHA256}", file=sys.stderr)
        return 1
    if len(written) != 148:
        print(f"length mismatch: got {len(written)} bytes, expected 148", file=sys.stderr)
        return 1
    if written.endswith(b"\n"):
        print("output must not end with a trailing newline", file=sys.stderr)
        return 1

    print(f"wrote {len(written)} bytes to {OUTPUT_PATH}, sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
