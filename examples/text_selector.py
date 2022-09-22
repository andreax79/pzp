#!/usr/bin/env python
import argparse
from pathlib import Path
from pzp import pzp
from pzp.layout import list_layouts

examples_dir = Path(__file__).parent
code_of_conduct = examples_dir.parent / "CODE_OF_CONDUCT.md"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--height", type=int)
    parser.add_argument("--layout", choices=list_layouts(), default="reverse-list")
    args = parser.parse_args()
    candidates = code_of_conduct.read_text().split("\n")
    item = pzp(
        candidates=candidates,
        layout=args.layout,
        fullscreen=args.fullscreen,
        height=args.height,
    )
    print(item)


if __name__ == "__main__":
    main()
