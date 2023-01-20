#!/usr/bin/env python
from pzp import prompt


def main():
    test = prompt("write something")
    print()
    print("-" * 100)
    print(test)


if __name__ == "__main__":
    main()
