#!/usr/bin/env python

import msvcrt
import threading
from typing import List, Optional

__all__ = ["get_char", "KEYS_MAPPING"]

NULL = "\0"
WIN_ESC = "\xe0"
KEYS_MAPPING = {
    "\xe0\x47": "home",
    "\xe0\x48": "up",
    "\xe0\x49": "pgup",
    "\xe0\x4b": "left",
    "\xe0\x4d": "right",
    "\xe0\x4f": "end",
    "\xe0\x50": "down",
    "\xe0\x51": "pgdn",
    "\xe0\x52": "insert",
    "\xe0\x53": "del",
    "\0\x3b": "f1",
    "\0\x3c": "f2",
    "\0\x3d": "f3",
    "\0\x3e": "f4",
    "\0\x3f": "f5",
    "\0\x40": "f6",
    "\0\x41": "f7",
    "\0\x42": "f8",
    "\0\x43": "f9",
    "\0\x44": "f10",
    "\0\x85": "f11",
    "\0\x86": "f12",
}


class TimeoutException(Exception):
    pass


def getwch(timeout: Optional[int] = None) -> str:
    if timeout is None:
        return msvcrt.getwch()  # type: ignore

    chars: List[str] = []

    def read_char() -> None:
        try:
            char = msvcrt.getwch()  # type: ignore
            chars.append(char)
        except Exception:
            pass

    read_thread = threading.Thread(target=read_char)
    read_thread.start()
    read_thread.join(timeout=timeout)
    if read_thread.is_alive():
        return ""
    return chars[0] if chars else ""


def get_char(timeout: Optional[int] = None) -> str:
    """
    Read a keypress and return the resulting character as a string.

    Returns:
        char: the pressed key or the key description (e.g. "home")
    """
    ch: str = getwch(timeout)
    if ch is None:
        return ""
    elif ch == WIN_ESC or ch == NULL:  # When reading arrow/insert/del key, the first call returnx 0xe0
        keys_mapping = KEYS_MAPPING
        while keys_mapping:
            ch = ch + getwch()
            keys_mapping = {k: v for k, v in keys_mapping.items() if k.startswith(ch)}
            if len(keys_mapping) == 1 and next(iter(keys_mapping.keys())) == ch:
                result = next(iter(keys_mapping.values()))
                return result
        return ""
    return ch
