#!/usr/bin/env python
import argparse
from pzp import Finder, GenericAction
from pzp.info import InfoStyle
from pzp.layout import list_layouts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", action=argparse.BooleanOptionalAction, default=False, help="toggle fullscreen")
    parser.add_argument("--info", choices=["default", "hidden"], default="hidden", help="determines the info style")
    parser.add_argument("--layout", choices=list_layouts(), default="reverse", help="choose the layout")
    args = parser.parse_args()
    info = InfoStyle.DEFAULT if args.info == "default" else InfoStyle.HIDDEN
    try:
        finder = Finder(
            candidates=["Yes", "No"],
            fullscreen=args.fullscreen,
            layout=args.layout,
            info_style=info,
        )
        finder.show()
    except GenericAction as action:
        print(action.selected_item)


if __name__ == "__main__":
    main()
