#!/usr/bin/env python
import argparse
from pzp import pzp, CustomAction, Layout
from pzp.layout import list_layouts


def num_format(item):
    return f"{item}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=1000)
    parser.add_argument("-f", "--fullscreen", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--height", type=int)
    parser.add_argument("--layout", choices=list_layouts(), default="reverse-list")
    args = parser.parse_args()
    try:
        item = pzp(
            candidates=range(0, args.n),
            layout=args.layout,
            format_fn=num_format,
            fullscreen=args.fullscreen,
            height=args.height,
            keys_binding={"custom": ["ctrl-o"], "qu-qu": ["ctrl-q"], "oh-oh": ["!"]},
            header_str="Press enter or ctrl-o",
        )
        print(item)
    except CustomAction as action:
        print(action.action)
        print(action.selected_item)


if __name__ == "__main__":
    main()
