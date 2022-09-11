#!/usr/bin/env python
from pathlib import Path
from pzp import pzp


def main():
    item = pzp(candidates=list(Path('.').iterdir()))
    print(str(item) if item else '')


if __name__ == "__main__":
    main()
