#!/usr/bin/env python3
"""Entry point for the make.fun "Meme Sprint 3: AI Agent Goes Rogue" bounty.

Copies the bundled entry.png (a fake dark-mode chat screenshot drawn
from scratch: a human asks their AI agent to tidy the downloads
folder; the agent does it, then sells the car, quits the human's job
for them, moves to the cloud and leaves the chat) to
$MAKEFUN_OUTPUT_DIR/entry.png.

Standard library only; deterministic: every run writes identical bytes.
The image itself is drawn by draw_meme.py (kept in this repository)
using only PIL primitives and DejaVu fonts.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = (
    "1bd44be3a5e001982f6e75d7ac183f49976bb2be7241593f4e4503f9bd26bf8e"
)


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    got = _sha256(dst)
    if got != EXPECTED_SHA256:
        print(f"error: sha256 mismatch: {got} != {EXPECTED_SHA256}",
              file=sys.stderr)
        return 1
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes, sha256 {got})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
