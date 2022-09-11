#!/usr/bin/env python
from pzp import pzp


def num_format(item):
    return f"{item}"


def main():
    line = pzp(candidates=range(0, 1000), format_fn=num_format)
    print(line)


if __name__ == "__main__":
    main()
