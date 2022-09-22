#!/usr/bin/env python

from typing import Any, Callable, Optional, TextIO
from .info import InfoStyle
from .ansi import (  # noqa
    NL,
    SPACE,
    ERASE_LINE,
    BLACK,
    RED,
    GREEN,
    YELLOW,
    BLUE,
    PURPLE,
    CYAN,
    WHITE,
    BLACK_BG,
    RED_BG,
    GREEN_BG,
    YELLOW_BG,
    BLUE_BG,
    PURPLE_BG,
    CYAN_BG,
    WHITE_BG,
    RESET,
    BOLD,
    NEGATIVE,
)

__all__ = ["Config"]


class Config:
    def __init__(
        self,
        fullscreen: bool,
        height: Optional[int],
        format_fn: Callable[[Any], str],
        info_style: InfoStyle,
        pointer_str: str,
        prompt_str: str,
        header_str: str,
        output_stream: TextIO,
    ):
        """
        Finder config

        Args:
            fullscreen: Full screen mode
            height: Finder window height
            format_fn: Items format function
            info_style: Determines the display style of finder info
            pointer_str: Pointer to the current line
            prompt_str: Input prompt
            header_str: Header
            output_stream: Output stream
        """
        self.fullscreen = fullscreen
        self.height = height
        self.format_fn = format_fn
        self.info_style: InfoStyle = info_style
        self.pointer_str = pointer_str
        self.no_pointer_str = " " * len(pointer_str)
        self.prompt_str = prompt_str
        self.header_str = header_str
        self.output_stream = output_stream

    @property
    def info_lines(self) -> int:
        "Number of info lines"
        return 1 if self.info_style == InfoStyle.DEFAULT else 0

    @property
    def prompt_lines(self) -> int:
        "Number of prompt lines"
        return len(self.prompt_str.split(f"{NL}"))

    @property
    def header_lines(self) -> int:
        "Number of header lines"
        return len(self.header_str.split(f"{NL}")) if self.header_str else 0

    @property
    def margin_lines(self) -> int:
        "Screen margin"
        return self.info_lines + self.prompt_lines + self.header_lines
