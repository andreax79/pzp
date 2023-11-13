#!/usr/bin/env python

import math
from abc import ABC, abstractmethod
from typing import Any, Dict, Sequence, Tuple, Type, Union

from .ansi import (  # noqa
    BLACK,
    BLACK_BG,
    BLUE,
    BLUE_BG,
    BOLD,
    CYAN,
    CYAN_BG,
    ERASE_LINE,
    GREEN,
    GREEN_BG,
    NEGATIVE,
    NL,
    PURPLE,
    PURPLE_BG,
    RED,
    RED_BG,
    RESET,
    SPACE,
    WHITE,
    WHITE_BG,
    YELLOW,
    YELLOW_BG,
    ansi_len,
)
from .candidates import Candidates
from .config import Config
from .info import InfoStyle
from .line_editor import LineEditor
from .screen import DummyScreen, Screen

__all__ = ["Layout", "DefaultLayout", "ReverseLayout", "ReverseListLayout", "get_layout", "list_layouts"]


layouts: Dict[str, Type["Layout"]] = {}


class Layout(ABC):
    def __init__(self, config: Config, candidates: Candidates):
        """
        Abstract layout

        Args:
            config: Configuration
            candidates: Candidates

        Attributes:
            config: Configuration
            candidates: Candidates
            offset: Screen offset
            line_editor: Line editor
            screen: Screen instance
        """
        self.config = config
        self.candidates = candidates
        self.offset: int = 0
        self.screen: Screen = DummyScreen()
        self.prompt_len: int = ansi_len(self.config.no_pointer_str) + 1

    def __init_subclass__(cls, option: str, **kwargs: Dict[str, Any]) -> None:
        "Register a subclass"
        super().__init_subclass__(**kwargs)
        layouts[option] = cls

    @abstractmethod
    def update_screen(self, selected: int, erase: bool = True) -> None:
        "Update the screen - erase the old items, print the filtered items and the prompt"
        pass  # pragma: no cover

    @abstractmethod
    def move_selection(self, selected: int, lines: int = 0, pages: int = 0) -> int:
        "Move selection up/down n lines/pages"
        pass  # pragma: no cover

    @abstractmethod
    def enumerate_items(self) -> Sequence[Tuple[int, Any]]:
        "Return a sequence of enumerated item to by displayed"
        pass  # pragma: no cover

    @abstractmethod
    def clear_screen(self, erase: bool) -> None:
        "Clean the screen"
        pass  # pragma: no cover

    def cleanup(self) -> None:
        "Clean the screen when the finder is closed"
        self.clear_screen(erase=True)
        self.screen.flush()

    @property
    def max_candidates_lines(self) -> int:
        "Maximun number of lines for printing the candidates"
        return self.screen.height - self.config.margin_lines

    @property
    def screen_items(self) -> Sequence[Any]:
        "Candidates to be displayed on the screen"
        items = []
        lines = 0
        for item in self.candidates.matching_candidates[self.offset :]:
            item_len = ansi_len(str(item)) + self.prompt_len
            lines += math.ceil(item_len / self.screen.width)
            if lines > self.max_candidates_lines:
                break
            items.append(item)
        return items

    @property
    def screen_items_lines(self) -> int:
        "Number of candidates lines (height on the screen)"
        lines = 0
        for item in self.screen_items:
            item_len = ansi_len(str(item)) + self.prompt_len
            lines += math.ceil(item_len / self.screen.width)
        return lines

    @property
    def screen_items_len(self) -> int:
        "Number of items on the screen"
        return len(self.screen_items)

    def screen_setup(self, line_editor: LineEditor) -> None:
        "Calculate the required height and setup the screen"
        self.line_editor = line_editor
        if self.config.height is not None:
            height: int = self.config.height
        else:
            # Calculate the required height
            height = self.config.margin_lines
            width = Screen.get_terminal_size().columns
            for item in self.candidates.candidates:
                item_len = ansi_len(str(item)) + self.prompt_len
                height += math.ceil(item_len / width)
        self.screen = Screen(stream=self.config.output_stream, fullscreen=self.config.fullscreen, height=height)
        self.update_screen(selected=0, erase=False)

    def calculate_offset(self, selected: int) -> None:
        "Calculate the screen offset"
        if selected >= self.offset + self.screen_items_len:
            self.offset = selected - self.screen_items_len + 1
        elif selected < self.offset:
            self.offset = selected
        if self.offset < 0:
            self.offset = 0

    def print_header(self) -> None:
        "Print header"
        if self.config.header_str:
            self.screen.erase_line().write(self.config.header_str).nl()

    def print_items(self, selected: int) -> None:
        "Print candidates"
        for i, item in self.enumerate_items():
            is_selected = i + self.offset == selected
            self.screen.erase_line()
            if is_selected:
                self.screen.write(f"{RED}{BOLD}{BLACK_BG}{self.config.pointer_str}").reset().bold()
            else:
                self.screen.write(f"{BLACK_BG}{self.config.no_pointer_str}").reset()
            self.screen.space(1).write(self.config.format_fn(item)).reset().nl()

    def print_empty_lines(self, delta: int = 0) -> None:
        "Print empty lines"
        lines = self.max_candidates_lines - self.screen_items_lines + delta
        self.screen.nl(lines)

    def print_info(self) -> None:
        "Print info"
        if self.config.info_style == InfoStyle.DEFAULT:
            matching_candidates_len = self.candidates.matching_candidates_len
            candidates_len = self.candidates.candidates_len
            self.screen.erase_line().space(2).write(f"{YELLOW}{matching_candidates_len}/{candidates_len}").reset().nl()

    def print_prompt(self) -> None:
        "Print prompt"
        self.screen.erase_line().write(f"{CYAN}{self.config.prompt_str}").reset()
        self.line_editor.print(self.screen)


class DefaultLayout(Layout, option="default"):
    "Display from the bottom of the screen"

    def update_screen(self, selected: int, erase: bool = True) -> None:
        "Update the screen - erase the old items, print the filtered items and the prompt"
        self.calculate_offset(selected)
        self.clear_screen(erase)
        self.print_header()
        self.print_empty_lines()
        self.print_items(selected)
        self.print_info()
        self.print_prompt()
        self.screen.flush()

    def enumerate_items(self) -> Sequence[Tuple[int, Any]]:
        "Return a sequence of enumerated item to by displayed"
        return reversed(list(enumerate(self.screen_items)))  # type: ignore

    def move_selection(self, selected: int, lines: int = 0, pages: int = 0) -> int:
        "Move selection up/down n lines"
        return selected + lines + pages * self.max_candidates_lines

    def clear_screen(self, erase: bool) -> None:
        "Clean the screen"
        if erase:
            lines = self.screen.height - 1
            self.screen.erase_line().move_up(lines).erase_lines(lines)


class ReverseLayout(Layout, option="reverse"):
    "Display from the top of the screen"

    def update_screen(self, selected: int, erase: bool = True) -> None:
        "Update the screen - erase the old items, print the filtered items and the prompt"
        self.calculate_offset(selected)
        self.clear_screen(erase)
        self.print_header()
        self.screen.nl()  # skip this line for the prompt
        self.print_info()
        self.print_items(selected)
        self.print_empty_lines(delta=-1 if self.config.fullscreen else 0)
        self.screen.move_up(self.max_candidates_lines + 1 + self.config.info_lines)  # jump back to the prompt line
        self.print_prompt()
        self.screen.flush()

    def enumerate_items(self) -> Sequence[Tuple[int, Any]]:
        "Return a sequence of enumerated item to by displayed"
        return list(enumerate(self.screen_items))

    def move_selection(self, selected: int, lines: int = 0, pages: int = 0) -> int:
        "Move selection up/down n lines"
        return selected - lines - pages * self.max_candidates_lines

    def clear_screen(self, erase: bool) -> None:
        "Clean the screen"
        if erase:
            lines: int = self.config.header_lines + self.config.prompt_lines - 2
            self.screen.move_up(lines)
            self.screen.erase_lines(self.screen.height)


class ReverseListLayout(ReverseLayout, option="reverse-list"):
    "Display from the top of the screen, prompt at the bottom"

    def update_screen(self, selected: int, erase: bool = True) -> None:
        "Update the screen - erase the old items, print the filtered items and the prompt"
        self.calculate_offset(selected)
        self.clear_screen(erase)
        self.print_header()
        self.print_items(selected)
        self.print_empty_lines()
        self.print_info()
        self.print_prompt()
        self.screen.flush()

    def clear_screen(self, erase: bool) -> None:
        "Clean the screen"
        if erase:
            lines = self.screen.height - 1
            self.screen.erase_line().move_up(lines).erase_lines(lines)


def get_layout(layout: Union[str, Type[Layout]], config: Config, candidates: Candidates) -> Layout:
    "Get a layout instance by name or by class"
    if isinstance(layout, str):
        return layouts[layout](config, candidates)
    else:
        return layout(config, candidates)


def list_layouts() -> Sequence[str]:
    "List layouts"
    return list(layouts.keys())
