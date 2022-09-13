#!/usr/bin/env python

import sys
from enum import Enum
from collections import ChainMap
from typing import Any, Callable, Iterator, Dict, Optional, Sequence, TextIO, Union
from .input import get_char
from .keys import ACTIONS, KEYS
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
    NORMAL,
    BOLD,
    NEGATIVE,
)
from .screen import Screen

__all__ = [
    "Finder",
    "Layout",
    "InfoStyle",
    "DEFAULT_POINTER",
    "DEFAULT_PROMPT",
]

DEFAULT_POINTER = ">"
"Default pointer"
DEFAULT_PROMPT = ">"
"Default input prompt"


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
        fullscreen: bool = True,
        height: Optional[int] = None,
        format_fn: Callable[[Any], str] = lambda x: str(x),
        layout: Layout = Layout.REVERSE_LIST,
        info_style: InfoStyle = InfoStyle.DEFAULT,
        pointer_str: str = DEFAULT_POINTER,
        prompt_str: str = DEFAULT_PROMPT,
        output_stream: TextIO = sys.stderr,
    ):
        """
        Initializate Finder object

        Args:
            candidates: Candidates
            fullscreen: Full screen mode
            height: Finder window height
            format_fn: Items format function
            layout: Finder layout
            info_style: Determines the display style of finder info
            pointer_str: Pointer to the current line
            prompt_str: Input prompt
        """
        self.fullscreen = fullscreen
        self.height = height
        self.format_fn = format_fn
        self.layout: Layout = layout
        self.info_style: InfoStyle = info_style
        self.pointer_str = pointer_str
        self.no_pointer_str = " " * len(pointer_str)
        self.prompt_str = prompt_str
        self.output_stream = output_stream
        self.keycodes_actions: Dict[str, str] = dict(ChainMap(*[{KEYS[v]: k for v in vlist} for k, vlist in ACTIONS.items()]))
        # Get the candidates
        if isinstance(candidates, Iterator) or callable(candidates):
            self.get_items_fn: Union[None, Callable[[], Sequence[Any]], Iterator[Any]] = candidates
            self.candidates: Sequence[Any] = []
        else:
            self.get_items_fn = None
            self.candidates = candidates

    def show(self, input: Optional[str] = None) -> Any:
        """
        Open pzp and return the selected element

        Args:
            input: initial search string

        Returns:
            item: the selected item
        """
        self.setup(input=input)
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
            self.screen.cleanup()

    @property
    def screen_items(self) -> Sequence[Any]:
        "Candidates to be displayed on the screen"
        return self.matching_candidates[self.offset : self.offset + self.max_candidates]

    @property
    def screen_items_len(self) -> int:
        "Number of items on the screen"
        return len(self.screen_items)

    @property
    def candidates_len(self) -> int:
        "Number of candidates"
        return len(self.candidates)

    @property
    def matching_candidates_len(self) -> int:
        "Number of matching candidates"
        return len(self.matching_candidates)

    @property
    def info_lines(self) -> int:
        "Number of info lines"
        return 1 if self.info_style == InfoStyle.DEFAULT else 0

    @property
    def prompt_lines(self) -> int:
        "Number of prompt lines"
        return len(self.prompt_str.split(f"{NL}"))

    @property
    def margin_lines(self) -> int:
        "Screen margin"
        return self.info_lines + self.prompt_lines

    @property
    def max_candidates(self) -> int:
        "Maximun number of candidates printables on the screen"
        return self.screen.height - self.margin_lines

    def setup(self, input: Optional[str] = None) -> None:
        """
        Setup Finder execution

        Args:
            input: initial search string
        """
        self.input: str = input or ""
        # Load the candidate list
        self.refresh_candidates()
        # Calculate the required height and setup the screen
        height = self.height if self.height is not None else self.candidates_len + self.margin_lines
        self.screen: Screen = Screen(stream=self.output_stream, fullscreen=self.fullscreen, height=height)
        # Filter the items, calculate the screen offset
        self.apply_filter()
        self.update_screen(erase=False)

    def refresh_candidates(self) -> None:
        "Load/reload the candidate list"
        # Get items
        if isinstance(self.get_items_fn, Iterator):
            self.candidates = list(self.get_items_fn)
        elif callable(self.get_items_fn):
            self.candidates = list(self.get_items_fn())
        # Reset selected/offset
        self.selected: int = 0
        self.offset: int = 0

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
            self.selected = self.selected + self.max_candidates
        elif action == "page-up":  # Move one page up
            self.selected = self.selected - self.max_candidates
        elif action == "backward-delete-char":  # Delete one characted
            if self.input:
                self.input = self.input[:-1]
        elif action == "ignore":  # Skip
            pass
        elif ch >= SPACE:  # Append the character to line
            self.input = self.input + ch

    def apply_filter(self) -> None:
        "Filter the items, calculate the screen offset"
        self.matching_candidates: Sequence[Any] = list(filter(self.match, self.candidates))
        # Adject selected
        self.selected = max(min(self.selected, self.matching_candidates_len - 1), 0)
        # Calculate the offset
        if self.selected >= self.offset + self.max_candidates:
            self.offset = self.selected - self.max_candidates + 1
        elif self.selected < self.offset:
            self.offset = self.selected
        if self.offset < 0:
            self.offset = 0

    def update_screen(self, erase: bool = True) -> None:
        "Update the screen - erase the old items, print the filtered items and the prompt"
        if erase:
            self.screen.erase_screen()
        if self.layout == Layout.REVERSE_LIST:
            self.print_items()
            self.print_empty_lines()
            self.print_info()
            self.print_prompt()
        self.screen.flush()

    def print_items(self) -> None:
        for i, item in enumerate(self.screen_items):
            is_selected = i + self.offset == self.selected
            if is_selected:
                self.screen.write(
                    f"{ERASE_LINE}{RED}{BOLD}{BLACK_BG}{self.pointer_str}{NORMAL} {BOLD}{self.format_fn(item)}{NORMAL}{NL}"
                )
            else:
                self.screen.write(f"{ERASE_LINE}{BLACK_BG}{self.no_pointer_str}{NORMAL} {self.format_fn(item)}{NL}")

    def print_empty_lines(self) -> None:
        if self.fullscreen:
            lines = self.max_candidates - self.screen_items_len
        else:
            lines = min(self.candidates_len, self.max_candidates - self.screen_items_len)
        self.screen.write(f"{NL}" * lines)

    def print_info(self) -> None:
        "Print info"
        if self.info_style == InfoStyle.DEFAULT:
            self.screen.write(f"  {ERASE_LINE}{YELLOW}{self.matching_candidates_len}/{self.candidates_len}{NORMAL}{NL}")

    def print_prompt(self) -> None:
        "Print prompt"
        self.screen.write(f"{ERASE_LINE}{CYAN}{self.prompt_str}{NORMAL} {self.input}")

    def match(self, item: Any) -> bool:
        return self.input.lower() in self.format_fn(item).lower()

    def prepare_result(self) -> Any:
        "Output the selected item, if any"
        try:
            return self.matching_candidates[self.selected]
        except IndexError:
            return None
