#!/usr/bin/env python
import os
import argparse
import random
from pzp import Finder, GenericAction
from pzp.layout import list_layouts
from pzp.info import list_styles


def row():
    columns = os.get_terminal_size().columns
    # return "".join([chr(97 + (i % 26)) for i in range(0, int(columns * 2.5))])
    return "".join([chr(random.randint(97, 97 + 25)) for i in range(0, int(columns * 2.5))])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", action=argparse.BooleanOptionalAction, default=False, help="toggle fullscreen")
    parser.add_argument("--info", choices=list_styles(), default="hidden", help="determines the info style")
    parser.add_argument("--layout", choices=list_layouts(), default="reverse", help="choose the layout")
    parser.add_argument("--rows", type=int, default=10, help="number of rows")
    args = parser.parse_args()

    candidates = [row() for _ in range(0, args.rows)]
    try:
        finder = Finder(
            candidates=candidates,
            fullscreen=args.fullscreen,
            layout=args.layout,
            info_style=args.info,
        )
        finder.show()
    except GenericAction as action:
        print(action.selected_item)


if __name__ == "__main__":
    main()
