#!/usr/bin/env python

from msvcrt import getwch  # type: ignore

__all__ = ["get_char"]

NULL = "\0"
WIN_ESC = "\xe0"
KEYS_MAPPING = {
    "\x47": "home",
    "\x48": "up",
    "\x49": "pgup",
    "\x4b": "left",
    "\x4d": "right",
    "\x4f": "end",
    "\x50": "down",
    "\x51": "pgdn",
    "\x52": "insert",
    "\x53": "del",
}


def get_char() -> str:
    """
    Read a keypress and return the resulting character as a string.

    Returns:
        char: the pressed key or the key description (e.g. "home")
    """
    ch: str = getwch()
    if ch == WIN_ESC:  # When reading arrow/insert/del key, the first call returnx 0xe0
        ch = getwch()  # The second call returns the key code
        return KEYS_MAPPING.get(ch, NULL)
    return ch
