#!/usr/bin/env python

import os
import sys
from typing import List, TextIO
from .ansi import (
    ESC,
    NL,
    SPACE,
    CURSOR_SAVE_POS,
    CURSOR_RESTORE_POS,
    ERASE_LINE,
    RED,
    GREEN,
    YELLOW,
    BLUE,
    PURPLE,
    CYAN,
    WHITE,
    NORMAL,
    BOLD,
    NEGATIVE,
)

__all__ = [
    "Screen",
    "ESC",
    "NL",
    "SPACE",
    "CURSOR_SAVE_POS",
    "CURSOR_RESTORE_POS",
    "ERASE_LINE",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "PURPLE",
    "CYAN",
    "WHITE",
    "NORMAL",
    "BOLD",
    "NEGATIVE",
]


class Screen:
    def __init__(self, stream: TextIO = sys.stderr):
        """
        Initialize screen

        Args:
            stream: output stream
        """
        self.stream: TextIO = stream
        self.data: List[str] = []
        self.height: int = os.get_terminal_size().lines

    def write(self, line: str) -> None:
        "Add data to be written on the stream"
        self.data.append(line)

    def flush(self) -> None:
        "Write data to the stream and flush it"
        self.stream.write("".join(self.data))
        self.data = []
        self.stream.flush()

    def init(self) -> None:
        "Save cursor position"
        self.write(f"{CURSOR_SAVE_POS}")
        self.flush()

    def cleanup(self, lines: int) -> None:
        "Clean screen and restore cursor position"
        self.write(f"{CURSOR_RESTORE_POS}")
        # self.move_up(lines)
        self.flush()

    def erase_lines(self, lines: int) -> None:
        "Erase n lines"
        self.move_up(lines)
        self.write(f"{ERASE_LINE}{NL}" * lines)
        self.move_up(lines)

    def move_up(self, lines: int) -> None:
        self.write(f"{ESC}[{lines}A")
