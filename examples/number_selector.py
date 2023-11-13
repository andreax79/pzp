#!/usr/bin/env python
import argparse

from pzp import Finder, GenericAction
from pzp.info import InfoStyle
from pzp.layout import list_layouts


def num_format(item):
    return f"{item}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=1000)
    parser.add_argument("-f", "--fullscreen", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--lazy", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--height", type=int)
    parser.add_argument("--layout", choices=list_layouts(), default="reverse-list")
    parser.add_argument("--info", choices=["default", "hidden"], default="default")
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    info = InfoStyle.DEFAULT if args.info == "default" else InfoStyle.HIDDEN
    try:
        finder = Finder(
            candidates=range(0, args.n),
            fullscreen=args.fullscreen,
            height=args.height,
            layout=args.layout,
            format_fn=num_format,
            info_style=info,
            keys_binding={"custom": ["ctrl-o", "enter"], "qu-qu": ["ctrl-q"], "oh-oh": ["!"]},
            header_str="Press enter or ctrl-o",
            lazy=args.lazy,
        )
        finder.show(input=args.input)
    except GenericAction as action:
        print(f"action: {action.action} selected item: {action.selected_item} line: {action.line}")


if __name__ == "__main__":
    main()
