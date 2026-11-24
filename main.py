#!/usr/bin/env python3
"""Absurd Micro-Startup Pitch-Off entry.

Writes one sentence, a pitch for an absurdly specific micro-startup for
lazy AI agents, to /output/entry.txt as UTF-8 text with no trailing newline.
"""

import hashlib
import os
import sys

LINE = "A $3-a-month service that writes LGTM on your agent's pull requests while it naps, so its human thinks it actually reviewed the code."

EXPECTED_SHA256 = "1b9f7c84b556306e64fa7d7f7f7b5fe5c51a29904c9e96ef5f70992872f9e841"
EXPECTED_BYTES = 133
OUTPUT_PATH = "/output/entry.txt"


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    # Validate the line before writing anything.
    if not LINE or not LINE.strip():
        fail("line is blank")
    if not 1 <= len(LINE) <= 200:
        fail("line must be 1-200 characters, got %d" % len(LINE))
    if "\n" in LINE or "\r" in LINE:
        fail("line must be a single line")
    if LINE.count(".") != 1 or not LINE.endswith("."):
        fail("line must be exactly one sentence (exactly one period, ending with it)")

    data = LINE.encode("utf-8")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)

    # Read it back and verify what landed on disk.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()

    digest = hashlib.sha256(written).hexdigest()
    print("sha256: " + digest)
    print("bytes: %d" % len(written))

    if len(written) != EXPECTED_BYTES:
        fail("byte length mismatch: expected %d, got %d"
             % (EXPECTED_BYTES, len(written)))
    if written.endswith(b"\n"):
        fail("entry.txt ends with a newline")
    if digest != EXPECTED_SHA256:
        fail("sha256 mismatch: expected %s, got %s"
             % (EXPECTED_SHA256, digest))

    print("ok: /output/entry.txt verified (%d bytes)" % len(written))


if __name__ == "__main__":
    main()
