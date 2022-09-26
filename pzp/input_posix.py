#!/usr/bin/env python

__all__ = ["get_char", "KEYS_MAPPING"]

import sys
import termios
import tty

NULL = "\0"
ESC = "\x1b"
KEYS_MAPPING = {
    "[A": "up",
    "[B": "down",
    "[C": "right",
    "[D": "left",
    "[Z": "btab",  # shift-tab
    "[1;2A": "shift-up",
    "[1;2B": "shift-down",
    "[1;2C": "shift-right",
    "[1;2D": "shift-left",
    "[1~": "home",
    "[2~": "insert",
    "[3~": "del",
    "[4~": "end",
    "[5~": "pgup",
    "[6~": "pgdn",
    "OP": "f1",
    "[11~": "f1",
    "OQ": "f2",
    "[12~": "f2",
    "OR": "f3",
    "[13~": "f3",
    "OS": "f4",
    "[14~": "f4",
    "[15~": "f5",
    "[17~": "f6",
    "[18~": "f7",
    "[19~": "f8",
    "[20~": "f9",
    "[21~": "f10",
    "[23~": "f11",
    "[24~": "f12",
}


def get_char() -> str:
    """
    Read a keypress and return the resulting character as a string.

    Returns:
        char: the pressed key or the key description (e.g. "home")
    """
    try:
        fd = sys.stdin.fileno()
        attrs = termios.tcgetattr(fd)
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == ESC:
            keys_mapping = KEYS_MAPPING
            ch = ""
            while keys_mapping:
                ch = ch + sys.stdin.read(1)
                keys_mapping = {k: v for k, v in keys_mapping.items() if k.startswith(ch)}
                if len(keys_mapping) == 1 and next(iter(keys_mapping.keys())) == ch:
                    result = next(iter(keys_mapping.values()))
                    return result
            return ""
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs)
