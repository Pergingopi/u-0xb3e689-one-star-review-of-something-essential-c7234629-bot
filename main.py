#!/usr/bin/env python3
"""One-star review of something essential: sleep.

Pure Python 3.13 standard library. The program writes one single-line
one-star review to /output/entry.txt. No network, no model call, fully
deterministic: the same code always writes the same bytes.

The review (80 characters, plus a trailing newline):
    I slept eight hours and woke up tired. This product does not work as advertised.

Format decisions (from the gate in the rules: entry.txt must be UTF-8 text
of 1 to 160 characters, not only white space, a single line):
- No star glyphs ("★☆☆☆☆") and no "1/5" in the file. The entry IS the
  one-star review body and the judge is already told every entry is a
  one-star review, so a rating would be filler that crowds the one joke
  (judge criterion 5). The review voice itself ("does not work as
  advertised") carries the one-star register.
- The file ends with one trailing newline, as in the template precedent.
  The review is a single line; the newline is a file terminator, not a
  second line. Even counting it, the file is 81 characters, far under
  the 160-character cap.
- No exclamation marks anywhere: the deadpan must do the work
  (judge criterion 3).

Candidate comparison (judge brief: funniest deadpan one-star review of
an everyday essential; the more essential the thing, the funnier):
1. Oxygen: "Oxygen is free and everywhere, yet I still run out of it
   climbing one flight of stairs." Most essential, sharp grievance,
   good turn at the end. Strong, but the complaint is about the
   reviewer's fitness as much as about oxygen.
2. Wi-Fi: "Wi-Fi works in every room except the one I am sitting in."
   Sharpest everyday annoyance and tightest line, but Wi-Fi is less
   essential than sleep, water or oxygen, so the joke has less weight.
3. Water: "Water has no taste, no smell, and no flavour, yet I am
   expected to drink eight glasses of it a day." True grievance, but
   it ends flat with no turn in the last few words.
4. Gravity: "Gravity has never once caught anything I dropped. It only
   makes sure it lands face down." Two beats; the second joke crowds
   the first, against criterion 5.
5. Mondays: "Mondays arrive on time every week. Nothing else in my
   life is this reliable, and I resent it." Clever turn, but the
   grievance is generic ("everyone hates Mondays"), not the sharpest
   true grievance nobody has written down.
6. Sleep (CHOSEN): "I slept eight hours and woke up tired. This
   product does not work as advertised." Sleep is a top-tier
   essential; the grievance (a full night's sleep, still tired) is
   universal, specific and instantly recognisable; the deadpan holds
   throughout; the sting lands in the last five words in authentic
   one-star-review voice; and it is one joke told cleanly.

Reviser check (24 Nov 2026): the sleep review was re-scored against
the brief's criteria in their stated priority order, with fresh
alternatives added (toilet, soap, sun, coffee). None beats it:
- Oxygen stays the closest rival, but its grievance is about the
  reviewer's own fitness, not about oxygen failing its job, so sleep
  wins on criterion 2 (sharpest true grievance in the thing itself).
- Toilet ("only clogs when guests are over") and soap ("smells like a
  meadow, dries my hands like a desert") are situational or two-beat,
  and both things are less essential than sleep, so they lose on
  criteria 1 and 5.
- The sun's best line ("free, on time every day, and still gives me
  sunburn") stacks two complaints and has no single turn, losing on
  criteria 4 and 5.
- Coffee ("promises energy and delivers a 3pm crash") is a known
  grievance, not a fresh one, and coffee is a stimulant, not one of
  the brief's named essentials, so it loses on criteria 1 and 2.
- Tighter sleep variants were also weighed: "I would like a refund"
  is punchier but states less than "does not work as advertised",
  which names the product's core promise failing and is the most
  canonical one-star phrasing; "Zero stars, would not recommend"
  contradicts the one-star framing. The builder's text stands.

Gate validation: validate_review() below enforces the gate before
anything is written, so a bad REVIEW can never reach the file: the
text must be one non-blank line, 1 to 160 characters, with no
newline or carriage return inside it, and no leading or trailing
whitespace. The check runs on every invocation, not just in tests.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

REVIEW = "I slept eight hours and woke up tired. This product does not work as advertised."

MAX_CHARS = 160


def validate_review(text):
    """Enforce the competition gate on the review text before writing.

    Raises AssertionError on any violation, so a bad REVIEW fails loudly
    instead of producing an invalid entry.txt.
    """
    assert isinstance(text, str), "review must be a string"
    assert text == text.strip(), "review must have no leading/trailing whitespace"
    assert text, "review must not be blank"
    assert len(text) <= MAX_CHARS, (
        f"review is {len(text)} characters, over the {MAX_CHARS} cap"
    )
    assert "\n" not in text and "\r" not in text, (
        "review must be a single line with no newline inside it"
    )


def main():
    validate_review(REVIEW)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = (REVIEW + "\n").encode("utf-8")
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, final)
    os.chmod(final, 0o644)


if __name__ == "__main__":
    main()
