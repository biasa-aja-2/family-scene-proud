"""Make the AI Judge Feel Proud: A Family Scene.

Writes one short family scene to /output/entry.txt.
Pure stdlib only (os, sys).
"""

import os
import sys

LINE = "Mum still saves the last dumpling for Dad, Dad still pretends not to notice, and thirty years on, neither of them has ever said it out loud."

MAX_CHARS = 280


def check_gate(line):
    """Gate: 1-280 chars, one or two lines, no control chars, not blank.

    Returns an error string, or None when the line passes.
    """
    if not line or not line.strip():
        return "line is empty or whitespace-only"
    if len(line) > MAX_CHARS:
        return "line is %d chars, over %d" % (len(line), MAX_CHARS)
    if line.count("\n") > 1 or "\r" in line:
        return "line count is not one or two"
    if any(ord(ch) < 32 and ch != "\n" for ch in line):
        return "line contains control characters"
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-check gate before writing anything.
    gate_error = check_gate(LINE)
    if gate_error is not None:
        print("gate failed: %s" % gate_error, file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    # Harden modes: the grader collects /output as another user, so the
    # file must stay readable (0644) and the directory traversable (0755).
    os.chmod(out_dir, 0o755)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    os.chmod(path, 0o644)

    # Read-back verification: byte-exact, valid UTF-8, no trailing newline.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("verification failed: file bytes differ", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if len(text) != len(LINE) or text.count("\n") > 1:
        print("verification failed: length or line check", file=sys.stderr)
        return 1
    if text.strip() != LINE or text != text.strip():
        print("verification failed: unexpected surrounding whitespace", file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
