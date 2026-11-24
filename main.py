"""The Funniest Out-of-Office.

Writes one out-of-office auto-reply to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
(default ``/output/entry.txt``). Pure stdlib, deterministic, no network.

The joke is one sharp incident in a deadpan voice, with no setup clause
and no second beat: the return date itself is the incident. Friday is
presented as a fixed return date, then the last words reveal it has
already been moved three times today, so the date is not a date at all,
just a promise that keeps sliding. A real person would set exactly this
line, and the punch lands in the final words.
"""

import os

ENTRY = "I'm out of office until Friday, a date I've moved three times today."


def is_single_line(text: str) -> bool:
    """True when the text holds no line break of either kind."""
    return "\n" not in text and "\r" not in text


def validate_entry(text: str) -> None:
    """Enforce the kit gate before anything is written.

    The gate requires UTF-8 text of 1 to 140 characters, not only
    whitespace, as a single line, so fail loudly here instead of
    writing an entry the gate would refuse.
    """
    if not text or text != text.strip():
        raise ValueError("entry must be non-empty with no surrounding whitespace")
    if len(text) > 140:
        raise ValueError(f"entry is {len(text)} characters, over the 140 cap")
    if not is_single_line(text):
        raise ValueError("entry must be a single line")


def output_path() -> str:
    """Directory the harness gives us, falling back to /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main() -> None:
    validate_entry(ENTRY)
    path = os.path.join(output_path(), "entry.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)


if __name__ == "__main__":
    main()
