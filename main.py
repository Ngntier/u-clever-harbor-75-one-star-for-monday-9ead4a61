"""One Star for Monday — make.fun entry.

Writes a single one-star review of Monday, written as if Monday were a
restaurant, to entry.txt in the output directory. Pure stdlib, deterministic:
the same bytes on every run.
"""

import os

# The line, chosen against the judge's brief (in the brief's own order):
#   1. Opens "One star." and reads as a restaurant review of Monday.
#   2. A real diner's complaint, all three elements: a server who forgot
#      the order, a dish (the special), and a bill that went wrong.
#   3. The joke is Monday-only: the bill comes with five more days —
#      no other day of the week can bill you for the rest of the week,
#      and "the special was a Monday meeting" names the day twice over.
#   4. Short and quotable: 123 characters, 23 words, one line — and the
#      smaller text wins exact ties, so there is no word to trim.
LINE = (
    "One star. The server forgot my order, the special was a Monday "
    "meeting, and the bill came with five more days. Never again."
)


def main() -> None:
    line = LINE
    # Gate validation: 1-180 characters, at most 25 words, a single line,
    # not only whitespace. The gate counts characters of the UTF-8 text, so
    # validate the decoded string and its exact byte round-trip (no stray
    # surrogates, no hidden control characters, no leading or trailing
    # whitespace to trim).
    if not (1 <= len(line) <= 180):
        raise ValueError(f"line is {len(line)} characters, must be 1-180")
    if len(line.split()) > 25:
        raise ValueError(f"line is {len(line.split())} words, must be <= 25")
    if line.strip() == "":
        raise ValueError("line must not be only whitespace")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line must not contain control characters")
    encoded = line.encode("utf-8")
    if encoded.decode("utf-8") != line:
        raise ValueError("line is not clean UTF-8")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exactly the line, no trailing newline, UTF-8.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Verify what landed on disk is byte-identical to what we intended.
    with open(path, "rb") as f:
        if f.read() != encoded:
            raise RuntimeError("entry.txt on disk does not match the line")


if __name__ == "__main__":
    main()
