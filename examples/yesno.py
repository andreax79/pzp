#!/usr/bin/env python
import argparse

from pzp import confirm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", action=argparse.BooleanOptionalAction, default=False, help="toggle fullscreen")
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    value = confirm(
        "Are you sure?",
        default=args.input != "no",
        fullscreen=args.fullscreen,
    )
    print("yes" if value else "no")


if __name__ == "__main__":
    main()
