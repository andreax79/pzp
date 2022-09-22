#!/usr/bin/env python
import argparse
from pathlib import Path
from pzp import pzp
from pzp.layout import list_layouts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--height", type=int)
    parser.add_argument("--layout", choices=list_layouts(), default="reverse-list")
    args = parser.parse_args()
    item = pzp(
        candidates=Path(".").iterdir(),
        layout=args.layout,
        fullscreen=args.fullscreen,
        height=args.height,
    )
    print(str(item) if item else "")


if __name__ == "__main__":
    main()
