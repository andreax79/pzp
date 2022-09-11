#!/usr/bin/env python

from pzp.input import get_char
from pzp.keys import KEYS

NULL = "\0"
UP = "↑"
DOWN = "↓"
RIGHT = "→"
LEFT = "←"

CR = "\r"
ESC = "\u001b"

keycodes = {v: k for k, v in KEYS.items()}
ch = ""
while ch != CR:
    ch = get_char()
    key = keycodes.get(ch)
    if len(ch) == 1:
        print(f"{ch} 0x{ord(ch):x} {key}")
    else:
        print(f"{ch} --- {key}")
    if ch == CR:  # or ch == ESC:
        break
