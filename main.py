"""One-line out-of-office reply writer.

Writes a single out-of-office auto-reply to ``entry.txt`` inside the
directory the harness provides (``$MAKEFUN_OUTPUT_DIR``, falling back
to ``/output``). Pure standard library, deterministic, no network.

The humour here is a deadpan confession tucked into the return date:
Friday sounds like a firm plan, until the closing words admit the
date has already slipped three times today. One incident, one voice,
and the punchline arrives at the very end, with nothing extra to cut.
"""

import os

ENTRY = "I'm out of office until Friday, a date I've moved three times today."


def is_single_line(text: str) -> bool:
    """Return True only when the text contains no line break at all."""
    return "\n" not in text and "\r" not in text


def validate_entry(text: str) -> None:
    """Check the line against the kit gate before writing anything.

    The gate wants UTF-8 text of 1 to 140 characters, more than just
    whitespace, on exactly one line. Refuse loudly here rather than
    handing the grader a file it would reject.
    """
    if not text or text != text.strip():
        raise ValueError("entry must be non-empty with no surrounding whitespace")
    if len(text) > 140:
        raise ValueError(f"entry is {len(text)} characters, over the 140 cap")
    if not is_single_line(text):
        raise ValueError("entry must be a single line")


def output_path() -> str:
    """Return the harness output directory, defaulting to /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main() -> None:
    """Validate the line, then write it out as entry.txt."""
    validate_entry(ENTRY)
    path = os.path.join(output_path(), "entry.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)


if __name__ == "__main__":
    main()
