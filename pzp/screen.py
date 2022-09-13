#!/usr/bin/env python

import shutil
import sys
from typing import List, Optional, TextIO
from .ansi import (  # noqa
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

__all__ = ["Screen"]

DEFAULT_HEIGHT = 24
"Default screen height"
DEFAULT_WIDTH = 80
"Default screen width"


class Screen:
    def __init__(self, stream: TextIO = sys.stderr, fullscreen: bool = True, height: Optional[int] = None):
        """
        Initialize screen

        Args:
            stream: Output stream
            fullscreen: Full screen mode
            height: Screen height
        """
        self.stream: TextIO = stream
        self.data: List[str] = []
        self.fullscreen = fullscreen
        if self.fullscreen or height is None:
            self.height: int = self.get_terminal_height()
        else:
            self.height = min(height, self.get_terminal_height())
        # Save cursor position
        self.write(f"{CURSOR_SAVE_POS}")
        self.flush()

    @classmethod
    def get_terminal_height(cls) -> int:
        return shutil.get_terminal_size(fallback=(DEFAULT_WIDTH, DEFAULT_HEIGHT)).lines

    def write(self, line: str) -> None:
        "Add data to be written on the stream"
        self.data.append(line)

    def flush(self) -> None:
        "Write data to the stream and flush it"
        self.stream.write("".join(self.data))
        self.data = []
        self.stream.flush()

    def cleanup(self) -> None:
        "Clean screen and restore cursor position"
        self.erase_screen()
        if self.fullscreen:
            self.write(f"{CURSOR_RESTORE_POS}")
            self.move_up(self.height - 1)
        self.flush()

    def erase_screen(self) -> None:
        "Erase the screen"
        lines: int = self.height - 1
        self.erase_lines(lines)

    def erase_lines(self, lines: int) -> None:
        """
        Erase n lines

        Args:
            lines: number of lines to be erased
        """
        self.move_up(lines)
        self.write(f"{ERASE_LINE}{NL}" * lines)
        self.move_up(lines)

    def move_up(self, lines: int) -> None:
        """
        Move cursor up
        If the cursor is already at the edge of the screen, this has no effect.

        Args:
            lines: number of lines
        """
        self.write(f"{ESC}[{lines}A")

    def move_down(self, lines: int) -> None:
        """
        Move cursor down
        If the cursor is already at the edge of the screen, this has no effect.

        Args:
            lines: number of lines
        """
        self.write(f"{ESC}[{lines}B")
