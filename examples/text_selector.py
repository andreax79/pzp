#!/usr/bin/env python
import argparse
from pathlib import Path
from pzp import pzp
from pzp.layout import list_layouts

examples_dir = Path(__file__).parent
code_of_conduct = examples_dir.parent / "CODE_OF_CONDUCT.md"


class LineItem:
    def __init__(self, i, line):
        self.i = i
        self.line = line

    def __str__(self):
        raise Exception("Cacca")
        return self.line


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("-n", "--line-numbers", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--height", type=int)
    parser.add_argument("--layout", choices=list_layouts(), default="reverse-list")
    args = parser.parse_args()
    candidates = code_of_conduct.read_text().split("\n")
    if args.line_numbers:
        item = pzp(
            candidates=[LineItem(i, line) for i, line in enumerate(candidates, start=1)],
            layout=args.layout,
            fullscreen=args.fullscreen,
            height=args.height,
            format_fn=lambda item: f"{item.i:3d}: {item.line}",
        )
        item = item.line if item else None
    else:
        item = pzp(
            candidates=candidates,
            layout=args.layout,
            fullscreen=args.fullscreen,
            height=args.height,
        )
    print(item)


if __name__ == "__main__":
    main()
