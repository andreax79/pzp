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
    RESET,
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

        Attributes:
            stream: Output stream
            data: Data to be written on the stream
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
        """
        Get the terminal height

        Returns:
            height: terminal height
        """
        return shutil.get_terminal_size(fallback=(DEFAULT_WIDTH, DEFAULT_HEIGHT)).lines

    def write(self, line: str) -> "Screen":
        "Add data to be written on the stream"
        self.data.append(line)
        return self

    def flush(self) -> "Screen":
        "Write data to the stream and flush it"
        self.stream.write("".join(self.data))
        self.data = []
        self.stream.flush()
        return self

    def cleanup(self) -> "Screen":
        "Clean screen and restore cursor position"
        self.erase_screen()
        if self.fullscreen:
            self.write(f"{CURSOR_RESTORE_POS}")
            self.move_up(self.height - 1)
        self.flush()
        return self

    def nl(self, lines: int = 1) -> "Screen":
        """
        Add n newlines

        Args:
            lines: number of newlines to be added
        """
        self.data.append(f"{NL}" * lines)
        return self

    def space(self, num: int = 1) -> "Screen":
        """
        Add n spaces

        Args:
            num: number of spaces
        """
        self.data.append(" " * num)
        return self

    def reset(self) -> "Screen":
        "Reset style and color"
        self.write(f"{RESET}")
        return self

    def bold(self) -> "Screen":
        "Set bold mode"
        self.write(f"{BOLD}")
        return self

    def erase_screen(self) -> "Screen":
        "Erase the screen"
        lines: int = self.height - 1
        return self.erase_line().move_up(lines).erase_lines(lines)

    def erase_line(self) -> "Screen":
        "Erase the current line"
        self.write(f"{ERASE_LINE}")
        return self

    def erase_lines(self, lines: int) -> "Screen":
        """
        Erase n lines

        Args:
            lines: number of lines to be erased
        """
        self.write(f"{ERASE_LINE}{NL}" * lines)
        return self.move_up(lines)

    def move_up(self, lines: int) -> "Screen":
        """
        Move cursor up
        If the cursor is already at the edge of the screen, this has no effect.

        Args:
            lines: number of lines
        """
        return self.write(f"{ESC}[{lines}A")

    def move_down(self, lines: int) -> "Screen":
        """
        Move cursor down
        If the cursor is already at the edge of the screen, this has no effect.

        Args:
            lines: number of lines
        """
        return self.write(f"{ESC}[{lines}B")

    def move_right(self, characters: int) -> "Screen":
        """
        Move cursor right
        If the cursor is already at the edge of the screen, this has no effect.

        Args:
            characters: number of characters
        """
        if characters > 0:
            return self.write(f"{ESC}[{characters}C")
        return self

    def move_left(self, characters: int) -> "Screen":
        """
        Move cursor left
        If the cursor is already at the edge of the screen, this has no effect.

        Args:
            characters: number of characters
        """
        if characters > 0:
            return self.write(f"{ESC}[{characters}D")
        return self
