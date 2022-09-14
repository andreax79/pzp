#!/usr/bin/env python

from collections import ChainMap
from typing import Dict, Optional, Sequence

__all__ = [
    "KEYS",
    "ACTIONS",
    "get_keycodes_actions",
]

KEYS = {
    "ctrl-a": "\x01",
    "ctrl-b": "\x02",
    "ctrl-c": "\x03",
    "ctrl-d": "\x04",
    "ctrl-e": "\x05",
    "ctrl-f": "\x06",
    "ctrl-g": "\x07",
    "ctrl-h": "\x08",
    "ctrl-i": "\x09",
    "ctrl-j": "\x0a",
    "ctrl-k": "\x0b",
    "ctrl-l": "\x0c",
    "ctrl-m": "\x0d",
    "ctrl-n": "\x0e",
    "ctrl-o": "\x0f",
    "ctrl-p": "\x10",
    "ctrl-q": "\x11",
    "ctrl-r": "\x12",
    "ctrl-s": "\x13",
    "ctrl-t": "\x14",
    "ctrl-u": "\x15",
    "ctrl-v": "\x16",
    "ctrl-w": "\x17",
    "ctrl-x": "\x18",
    "ctrl-y": "\x19",
    "ctrl-z": "\x1a",
    "ctrl-\\": "\x1c",
    "ctrl-]": "\x1d",
    "ctrl-^": "\x1e",
    "ctrl-/": "\x1f",
    "pgup": "pgup",
    "page-up": "pgup",
    "pgdn": "pgdn",
    "page-down": "pgdn",
    "insert": "insert",
    "del": "del",
    "space": " ",
    "null": "\0",
    "up": "up",
    "down": "down",
    "right": "right",
    "left": "left",
    "home": "home",
    "end": "end",
    "nl": "\n",
    "enter": "\r",
    "tab": "\t",
    "bspace": "\x7f",
    "esc": "\x1b",
}

ACTIONS = {
    "abort": ["ctrl-c", "ctrl-g", "ctrl-q", "esc"],
    "accept": ["enter"],
    "backward-delete-char": ["ctrl-h", "bspace"],
    "delete-char": ["ctrl-d", "del"],
    "down": ["ctrl-j", "ctrl-n", "down"],
    "up": ["ctrl-k", "ctrl-p", "up"],
    "ignore": ["null", "insert"],
    "page-up": ["page-up", "pgup"],
    "page-down": ["page-down", "pgdn"],
    "backward-char": ["ctrl-b", "left"],
    "forward-char": ["ctrl-f", "right"],
    "beginning-of-line": ["ctrl-a", "home"],
    "end-of-line": ["ctrl-e", "end"],
}


def get_keycodes_actions(actions: Optional[Dict[str, Sequence[str]]] = None) -> Dict[str, str]:
    """
    Get keycodes to actions mapping

    Args:
        actions: Custom key binding

    Returns:
        keycodes_actions: key => action mapping
    """
    if actions is not None:
        actions_items = dict(ACTIONS, **actions).items()
    else:
        actions_items = ACTIONS.items()
    return dict(ChainMap(*[{KEYS[v]: k for v in vlist} for k, vlist in actions_items]))
