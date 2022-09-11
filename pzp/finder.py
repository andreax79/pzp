#!/usr/bin/env python

from enum import Enum
from collections import ChainMap
from typing import Any, Callable, Iterator, Dict, List, Optional, Sequence, Union
from .input import get_char
from .keys import ACTIONS, KEYS
from .ansi import (
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
    NORMAL,
    BOLD,
    NEGATIVE,
)
from .screen import Screen

__all__ = [
    "Finder",
    "Layout",
    "InfoStyle",
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
    "NORMAL",
    "BOLD",
    "NEGATIVE",
]


class Confirm(Exception):
    pass


class Cancel(Exception):
    pass


class Layout(Enum):
    "Finder layouts"
    REVERSE_LIST = "reverse-list"
    " Display from the top of the screen, prompt at the bottom "


class InfoStyle(Enum):
    "Display style of finder info"

    DEFAULT = "default"
    " Display on the next line to the prompt "
    HIDDEN = "hidden"
    " Do not display finder info"


class Finder:
    def __init__(
        self,
        candidates: Union[Callable[[], Sequence[Any]], Iterator[Any], Sequence[Any]],
        max_lines: Optional[int] = None,
        format_fn: Callable[[Any], str] = lambda x: str(x),
        layout: Layout = Layout.REVERSE_LIST,
        info_style: InfoStyle = InfoStyle.DEFAULT,
    ):
        self.format_fn = format_fn
        self.screen: Screen = Screen()
        self.layout: Layout = layout
        self.info_style: InfoStyle = info_style
        self.keycodes_actions: Dict[str, str] = dict(ChainMap(*[{KEYS[v]: k for v in vlist} for k, vlist in ACTIONS.items()]))
        # Calculate max lines
        if max_lines is None:
            margin = self.info_lines + 1  # info lines + prompt
            self.max_lines = self.screen.height - margin
        else:
            self.max_lines = max_lines
        # Get the candidates
        if isinstance(candidates, Iterator) or callable(candidates):
            self.get_items_fn: Union[None, Callable[[], Sequence[Any]], Iterator[Any]] = candidates
        else:
            self.get_items_fn = None
            self.candidates: Sequence[Any] = candidates
        self.refresh_candidates()

    def show(self, input: Optional[str] = None) -> Any:
        """
        Open pzp and return the selected element

        Args:
            input: initial search string

        Returns:
            item: the selected item
        """
        self.input: str = input or ""
        self.selected: int = 0
        self.offset: int = 0
        self.screen_items: List[Any] = []
        self.screen.init()
        self.apply_filter()
        self.update_screen(erase=False)
        try:
            while True:
                self.process_key(get_char())
                self.apply_filter()
                self.update_screen()
        except Confirm:
            return self.prepare_result()
        except Cancel:
            return None
        finally:
            self.screen.erase_lines(self.max_lines + self.info_lines)
            self.screen.cleanup(self.max_lines + self.info_lines)

    @property
    def screen_items_len(self) -> int:
        "Number of items on the screen"
        return len(self.screen_items) if self.screen_items else 0

    @property
    def info_lines(self) -> int:
        "Number of info lines"
        return 1 if self.info_style == InfoStyle.DEFAULT else 0

    def refresh_candidates(self) -> None:
        "Load/reload the candidate list"
        # Get items
        if isinstance(self.get_items_fn, Iterator):
            self.candidates = list(self.get_items_fn)
        elif callable(self.get_items_fn):
            self.candiates = self.get_items_fn()

    def process_key(self, ch: str) -> None:
        "Process the pressed key"
        action = self.keycodes_actions.get(ch)
        if action == "accept":  # Confirm
            raise Confirm
        elif action == "abort":  # Cancel
            raise Cancel
        elif action == "down":  # Move one line down
            self.selected = self.selected + 1
        elif action == "up":  # Move one line up
            self.selected = self.selected - 1
        elif action == "page-down":  # Move one page down
            self.selected = self.selected + self.max_lines
        elif action == "page-up":  # Move one page up
            self.selected = self.selected - self.max_lines
        elif action == "backward-delete-char":  # Delete one characted
            if self.input:
                self.input = self.input[:-1]
        elif action == "ignore":  # Skip
            pass
        elif ch >= SPACE:  # Append the character to line
            self.input = self.input + ch

    def apply_filter(self) -> None:
        "Filter the items, calculate the screen offset"
        self.filtered_items: Sequence[Any] = list(filter(self.match, self.candidates))
        self.selected = max(min(self.selected, len(self.filtered_items) - 1), 0)
        # Calculate the offset
        if self.selected >= self.offset + self.max_lines:
            self.offset = self.selected - self.max_lines + 1
        elif self.selected < self.offset:
            self.offset = self.selected
        if self.offset < 0:
            self.offset = 0
        # Items to be displayed
        self.screen_items = self.filtered_items[self.offset : self.offset + self.max_lines]

    def update_screen(self, erase: bool = True) -> None:
        "Update the screen - erase the old items, print the filtered items and the prompt"
        if erase:
            self.screen.erase_lines(self.max_lines + self.info_lines)
        if self.layout == Layout.REVERSE_LIST:
            self.print_items()
            self.print_empty_lines()
            self.print_info()
            self.print_prompt()
        self.screen.flush()

    def print_items(self) -> None:
        for i, item in enumerate(self.screen_items):
            if i + self.offset == self.selected:
                self.screen.write(f"{ERASE_LINE}{RED}{BOLD}{BLACK_BG}>{NORMAL} {BOLD}{self.format_fn(item)}{NORMAL}{NL}")
            else:
                self.screen.write(f"{ERASE_LINE}{BLACK_BG} {NORMAL} {self.format_fn(item)}{NL}")

    def print_empty_lines(self) -> None:
        self.screen.write(f"{NL}" * (min(len(self.candidates), self.max_lines - self.screen_items_len)))

    def print_info(self) -> None:
        "Print info"
        if self.info_style == InfoStyle.DEFAULT:
            self.screen.write(f"  {ERASE_LINE}{YELLOW}{len(self.filtered_items)}/{len(self.candidates)}{NORMAL}{NL}")

    def print_prompt(self) -> None:
        "Print prompt"
        self.screen.write(f"{ERASE_LINE}{CYAN}>{NORMAL} {self.input}")

    def match(self, item: Any) -> bool:
        return self.input.lower() in self.format_fn(item).lower()

    def prepare_result(self) -> Any:
        "Output the selected item, if any"
        try:
            return self.filtered_items[self.selected]
        except IndexError:
            return None
