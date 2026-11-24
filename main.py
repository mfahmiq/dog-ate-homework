"""The Dog Ate My Homework: Funniest Excuse — make.fun text bounty entry.

Writes one funny single-line excuse, in a dog's own voice, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Deterministic, Python standard library only. Self-verifies the entry
against the same rules the make.fun gate applies: UTF-8 text, 1-200
characters, a single line, not whitespace-only. Exits non-zero on
any failure.

The verification lives in verify_entry(), a small pure function that
returns every problem it finds instead of stopping at the first one,
so a single run reports the whole story instead of forcing a
fix-one-rerun-fix-one loop. The file written to disk is re-read and
re-checked with those same rules, so the bytes on disk — not just the
string in memory — are proven gate-valid.
"""

import os
import sys

ENTRY = (
    "You wrote my name on it, so legally it was mine — "
    "and in this house, anything that is mine gets eaten."
)

MAX_ENTRY_CHARS = 200


def verify_entry(text):
    """Check one candidate entry against the gate rules.

    Returns a list of problem strings; an empty list means the entry
    is valid. Every rule runs even when an earlier one failed, so one
    run reports all problems at once instead of bailing on the first.
    """
    problems = []

    if not isinstance(text, str):
        return [f"entry must be text, got {type(text).__name__}"]

    # UTF-8: the gate reads the file as UTF-8 text, so a character
    # that cannot be encoded — a lone surrogate, for example — fails
    # even though the string itself exists happily in memory.
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"entry is not valid UTF-8: {exc}")

    # Length is counted in characters, not bytes: the gate says
    # 1-200 characters, and the entry's em dash is one character but
    # three bytes, so a byte count would wrongly reject it.
    if not 1 <= len(text) <= MAX_ENTRY_CHARS:
        problems.append(
            f"entry is {len(text)} chars, must be 1-{MAX_ENTRY_CHARS}"
        )

    # A single line means no line breaks of either kind: a bare
    # carriage return would still split the line for a reader.
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")

    # Whitespace-only covers the empty-looking entry: spaces, tabs,
    # or exotic Unicode spaces that strip() removes.
    if not text.strip():
        problems.append("entry must not be whitespace-only")

    return problems


def report_problems(problems):
    """Print every problem as its own FAIL line; return 1 if any."""
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    return 1 if problems else 0


def verify_written_file(output_path):
    """Re-read the written file and check it with the gate rules.

    Returns a list of problem strings; an empty list means the file
    on disk is byte-identical to the entry plus one trailing newline
    AND its text passes verify_entry(). Checking the round-tripped
    text — not only comparing bytes — proves the file itself is
    gate-valid: a write path that translated newlines, substituted an
    unencodable character, or appended an extra terminator would
    still produce bytes that differ, but the re-check also catches
    the case where the bytes look plausible yet the text violates a
    rule (for instance a second newline hiding after the terminator).
    """
    try:
        # newline="" disables universal-newline translation, so what
        # we read is exactly what is on disk, byte for byte.
        with open(output_path, "r", encoding="utf-8", newline="") as fh:
            written = fh.read()
    except OSError as exc:
        return [f"cannot re-read written file {output_path}: {exc}"]
    except UnicodeDecodeError as exc:
        return [f"written file is not valid UTF-8: {exc}"]

    if written != ENTRY + "\n":
        return ["written file does not match the entry"]

    # Strip exactly the one trailing newline this program adds, then
    # run the file's own text through the same gate rules.
    round_tripped = written[:-1]
    return [
        f"written file: {problem}" for problem in verify_entry(round_tripped)
    ]


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = os.path.join(output_dir, "entry.txt")

    # 1. Check the entry in memory, reporting every problem at once.
    # No file is written while the entry is invalid.
    problems = verify_entry(ENTRY)
    if problems:
        return report_problems(problems)

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY + "\n")

    # 2. Re-read the file and re-check it with the same rules, so the
    # file on disk — not just the string in memory — is gate-valid.
    problems = verify_written_file(output_path)
    if problems:
        return report_problems(problems)

    print(f"OK: wrote {len(ENTRY)}-char entry to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
