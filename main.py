"""Publish the 24 November 2026 front page to the harness output folder.

Reads the committed entry.png sitting next to this file and writes an
identical copy into MAKEFUN_OUTPUT_DIR (or /output when unset). The copy
is checked by size and SHA-256 before success is reported, so a
truncated or altered write is caught instead of shipped silently.
"""

import hashlib
import os
import pathlib
import sys

PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    # entry.png sits next to this file in the repository checkout.
    root = pathlib.Path(__file__).resolve().parent
    source = root / "entry.png"
    if not source.is_file():
        fail(f"entry image missing: {source}")
    data = source.read_bytes()
    if not data.startswith(PNG_MAGIC):
        fail(f"not a PNG image: {source}")
    out_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    written = target.read_bytes()
    if len(written) != len(data) or sha256_hex(written) != sha256_hex(data):
        fail(f"verification failed after writing {target}")
    print(f"wrote {target} size={len(data)} sha256={sha256_hex(data)}")


main()
