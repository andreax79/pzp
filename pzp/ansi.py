#!/usr/bin/env python

__all__ = [
    "ESC",
    "NL",
    "SPACE",
    "CURSOR_SAVE_POS",
    "CURSOR_RESTORE_POS",
    "ERASE_LINE",
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "PURPLE",
    "CYAN",
    "WHITE",
    "BLACK_BG",
    "RED_BG",
    "GREEN_BG",
    "YELLOW_BG",
    "BLUE_BG",
    "PURPLE_BG",
    "CYAN_BG",
    "WHITE_BG",
    "RESET",
    "BOLD",
    "NEGATIVE",
]

ESC = "\u001b"
NL = "\n"
SPACE = " "

CURSOR_SAVE_POS = f"{ESC}7"
"Save cursor position"
CURSOR_RESTORE_POS = f"{ESC}8"
"Restores the cursor to the last saved position"
ERASE_LINE = f"{ESC}[2K"
"Erase the entire line"

BLACK = f"{ESC}[30m"
"Black foreground color"
RED = f"{ESC}[31m"
"Red foreground color"
GREEN = f"{ESC}[32m"
"Green foreground color"
YELLOW = f"{ESC}[33m"
"Yellow foreground color"
BLUE = f"{ESC}[34m"
"Blue foreground color"
PURPLE = f"{ESC}[35m"
"Purple foreground color"
CYAN = f"{ESC}[36m"
"Cyan foreground color"
WHITE = f"{ESC}[37m"
"White foreground color"

BLACK_BG = f"{ESC}[40m"
"Black background color"
RED_BG = f"{ESC}[41m"
"Red background color"
GREEN_BG = f"{ESC}[42m"
"Green background color"
YELLOW_BG = f"{ESC}[43m"
"Yellow background color"
BLUE_BG = f"{ESC}[44m"
"Blue background color"
PURPLE_BG = f"{ESC}[45m"
"Purple background color"
CYAN_BG = f"{ESC}[46m"
"Cyan background color"
WHITE_BG = f"{ESC}[47m"
"White background color"

RESET = f"{ESC}[0m"
"Reset styles and colors"
BOLD = f"{ESC}[1m"
"Set bold mode"
NEGATIVE = f"{ESC}[7m"
"Set inverse mode"
