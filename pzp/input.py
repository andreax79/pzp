#!/usr/bin/env python

import sys

__all__ = ["get_char"]

NULL = "\0"

try:
    import termios
    import tty

    ESC = "\u001b"

    def get_char() -> str:
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
                    elif ch == "2":
                        ch = "insert"
                        sys.stdin.read(1)  # skip ~
                    elif ch == "3":
                        ch = "del"
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

except ImportError:
    try:
        from msvcrt import getch  # type: ignore

        WIN_ESC = "\xe0"

        def get_char() -> str:
            ch: str = getch()
            if ch == WIN_ESC:
                ch = sys.stdin.read(1)
                if ch == "H":
                    ch = "up"
                elif ch == "P":
                    ch = "down"
                elif ch == "M":
                    ch = "right"
                elif ch == "K":
                    ch = "left"
                elif ch == "R":
                    ch = "insert"
                elif ch == "S":
                    ch = "del"
                elif ch == "I":
                    ch = "pgup"
                elif ch == "Q":
                    ch = "pgdn"
                else:
                    ch = NULL
            return ch

    except ImportError:
        pass
