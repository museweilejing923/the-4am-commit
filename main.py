"""The 4 a.m. commit writer.

Writes one fixed commit message about a 3 a.m. typo to
/output/entry.txt. Same bytes every run: no input, no clock,
no network, no randomness.
"""

import os
import string
import sys

MESSAGE = "fix: I found the bug at 4 a.m. It was a typo I wrote at 3 a.m. I have apologised to the tests."
CEILING = 200


def has_glued_sentence(line):
    """True when one sentence runs straight into the next.

    A full stop, exclamation or question mark must be followed by
    a space, never glued onto the next word (".It"). Only a capital
    letter counts as the next sentence starting, so "a.m." is fine.
    """
    for current, following in zip(line, line[1:]):
        if current in ".!?" and following.isupper():
            return True
    return False


def first_problem(line):
    if line.strip() == "":
        return "empty commit message"
    if len(line) > CEILING:
        return "over the 200-character limit"
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        return "control character inside"
    if line.strip() != line or "  " in line or "\n" in line:
        return "ragged spacing or a line break"
    if line[-1] not in ".!?":
        return "no closing punctuation"
    if all(ch in string.punctuation for ch in line):
        return "punctuation only"
    if line.isdigit():
        return "digits only"
    if not any(ch.isalpha() for ch in line):
        return "no letters"
    if not line.startswith("fix:"):
        return "not a fix: commit message"
    if has_glued_sentence(line):
        return "two sentences glued together with no space"
    return None


def main():
    problem = first_problem(MESSAGE)
    if problem is not None:
        print("error: " + problem, file=sys.stderr)
        raise SystemExit(1)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as out:
        out.write(MESSAGE + "\n")


if __name__ == "__main__":
    main()
