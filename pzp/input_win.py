#!/usr/bin/env python

import sys

__all__ = ["get_char"]

from msvcrt import getwch  # type: ignore

NULL = "\0"
WIN_ESC = "\xe0"
KEYS_MAPPING = {
    "H": "up",
    "P": "down",
    "M": "right",
    "K": "left",
    "R": "insert",
    "S": "del",
    "I": "pgup",
    "Q": "pgdn",
}


def get_char() -> str:
    ch: str = getwch()
    if ch == WIN_ESC:
        ch = sys.stdin.read(1)
        return KEYS_MAPPING.get(ch, NULL)
    return ch
