#!/usr/bin/env python

__all__ = ["get_char"]

import sys
import termios
import tty

NULL = "\0"
ESC = "\x1b"


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
            ch = sys.stdin.read(1)
            if ch == "[":
                ch = sys.stdin.read(1)
                if ch == "A":
                    ch = "up"
                elif ch == "B":
                    ch = "down"
                elif ch == "C":
                    ch = "right"
                elif ch == "D":
                    ch = "left"
                elif ch == "1":
                    ch = "home"
                    sys.stdin.read(1)  # skip ~
                elif ch == "2":
                    ch = "insert"
                    sys.stdin.read(1)  # skip ~
                elif ch == "3":
                    ch = "del"
                    sys.stdin.read(1)  # skip ~
                elif ch == "4":
                    ch = "end"
                    sys.stdin.read(1)  # skip ~
                elif ch == "5":
                    ch = "pgup"
                    sys.stdin.read(1)  # skip ~
                elif ch == "6":
                    ch = "pgdn"
                    sys.stdin.read(1)  # skip ~
                else:
                    ch = NULL
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs)
