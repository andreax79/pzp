#!/usr/bin/env python

from pzp.input import get_char
from pzp.keys import KEYS

CR = "\r"

keycodes = {v: k for k, v in KEYS.items()}
ch = ""
print("Press enter to exit")
while ch != CR:
    ch = get_char()
    key = keycodes.get(ch)
    if len(ch) == 1:
        print(f"{ch} 0x{ord(ch):x} {key}")
    else:
        print(f"{ch} --- {key}")
    if ch == CR:  # or ch == ESC:
        break
