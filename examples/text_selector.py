#!/usr/bin/env python
import argparse
from pathlib import Path
from pzp import pzp

examples_dir = Path(__file__).parent
code_of_conduct = examples_dir.parent / "CODE_OF_CONDUCT.md"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--height", type=int)
    args = parser.parse_args()
    candidates = code_of_conduct.read_text().split("\n")
    item = pzp(
        candidates=candidates,
        fullscreen=args.fullscreen,
        height=args.height,
    )
    print(item)


if __name__ == "__main__":
    main()
