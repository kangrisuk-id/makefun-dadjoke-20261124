#!/usr/bin/env python3
"""Dad Joke Showdown — write this entry's one dad joke to entry.txt.

Pure standard library. The joke is chosen in candidates.md by a pairwise
tournament run against the judge's published criteria, in their order.
"""

import os
import sys

JOKE = "What do you call a dad who falls through the ice? A popsicle."


def output_candidates():
    """Yield the places to try for entry.txt, best first."""
    seen = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        seen.append(env_dir)
    seen.append("/output")
    seen.append(os.path.join(os.getcwd(), "output"))
    seen.append(os.getcwd())
    out = []
    for path in seen:
        if path and path not in out:
            out.append(path)
    return out


def main():
    payload = (JOKE + "\n").encode("utf-8")
    errors = []
    for directory in output_candidates():
        try:
            os.makedirs(directory, exist_ok=True)
            target = os.path.join(directory, "entry.txt")
            with open(target, "wb") as handle:
                handle.write(payload)
            print(f"wrote {target} ({len(JOKE)} characters)")
            return 0
        except OSError as exc:
            errors.append(f"{directory}: {exc}")
    for line in errors:
        print(f"could not write: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
