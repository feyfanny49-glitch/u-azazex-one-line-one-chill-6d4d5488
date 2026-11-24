#!/usr/bin/env python3
"""One Line, One Chill: atomically write the one judged text to /output/entry.txt.

The judged artifact is the file's exact bytes: UTF-8, 1-200 characters, no
trailing newline. The grader refuses a mode-600 file, so the temp file is
chmod'd 0644 before os.replace. Stdlib only; no network in the sandbox.
"""

import hashlib
import os
import tempfile

ARTIFACT = "/output/entry.txt"

ENTRY = ("The bathtub was full when I got home; the taps were dry, "
         "and the water was still warm from a body.")


def validate(text: str) -> bytes:
    """Return the exact artifact bytes, or raise if the gate would reject it."""
    data = text.encode("utf-8")
    decoded = data.decode("utf-8")  # prove the bytes are valid UTF-8
    if decoded != text:
        raise ValueError("entry is not a clean UTF-8 round-trip")
    if not (1 <= len(decoded) <= 200):
        raise ValueError("entry must be 1-200 characters, got %d" % len(decoded))
    if not decoded.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in decoded or "\r" in decoded:
        raise ValueError("entry must be one line with no trailing newline")
    return data


def write_atomically(data: bytes) -> None:
    out_dir = os.path.dirname(ARTIFACT)
    os.makedirs(out_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, 0o644)  # never let a 0600 tempfile become the artifact
        os.replace(tmp, ARTIFACT)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main() -> None:
    data = validate(ENTRY)
    write_atomically(data)

    final = open(ARTIFACT, "rb").read()
    if final != data:
        raise ValueError("artifact bytes differ from the chosen entry")
    mode = os.stat(ARTIFACT).st_mode & 0o777
    if mode != 0o644:
        raise ValueError("artifact mode is %o, expected 644" % mode)
    print("artifact: %s" % ARTIFACT)
    print("chars=%d bytes=%d mode=0%o sha256=%s"
          % (len(final.decode("utf-8")), len(final), mode,
             hashlib.sha256(final).hexdigest()))
    print("text=%s" % final.decode("utf-8"))


if __name__ == "__main__":
    main()
