#!/usr/bin/env python

__all__ = ["get_char", "KEYS_MAPPING"]

import os
import signal
import sys
import termios
import tty
from typing import Any, Optional

NULL = "\0"
ESC = "\x1b"
KEYS_MAPPING = {
    "": ESC,
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


class TimeoutException(Exception):
    pass


def timeout_handler(signum: int, frame: Any) -> None:
    raise TimeoutException


def get_char(timeout: Optional[int] = None) -> Optional[str]:
    """
    Read a keypress and return the resulting character as a string.

    Args:
        timeout (Optional[int]): The time in seconds to wait for input before timing out. Defaults to None.

    Returns:
        char: the pressed key or the key description (e.g. "home")
    """
    fd = None
    try:
        fd = sys.stdin.fileno()
        attrs = termios.tcgetattr(fd)
        tty.setraw(fd)

        if timeout is not None:
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, timeout)

        try:
            ch = os.read(fd, 32).decode("utf-8", "replace")
        except TimeoutException:
            ch = NULL

        if timeout is not None:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old_handler)

        if ch is not None and ch.startswith(ESC):
            ch = KEYS_MAPPING.get(ch[1:], NULL)
        return ch
    finally:
        if fd is not None:
            termios.tcsetattr(fd, termios.TCSAFLUSH, attrs)
