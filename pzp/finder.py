#!/usr/bin/env python

import sys
from enum import Enum
from typing import Any, Callable, Iterator, Optional, Sequence, TextIO, Type, Union
from .keys import KeyEvent, KeysBinding
from .exceptions import AcceptAction, AbortAction, CustomAction, MissingHander
from .line_editor import LineEditor
from .actions import Action, ActionsHandler
from .matcher import Matcher, ExtendedMatcher
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
from .screen import Screen

__all__ = [
    "Finder",
    "CustomAction",
    "Layout",
    "InfoStyle",
    "DEFAULT_POINTER",
    "DEFAULT_PROMPT",
    "DEFAULT_HEADER",
]

DEFAULT_POINTER = ">"
"Default pointer"
DEFAULT_PROMPT = "> "
"Default input prompt"
DEFAULT_HEADER = ""
"Default header"


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


class Finder(ActionsHandler):
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
        header_str: str = DEFAULT_HEADER,
        keys_binding: Optional[KeysBinding] = None,
        matcher: Union[Matcher, Type[Matcher]] = ExtendedMatcher,
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
            header_str: Header
            keys_binding: Custom keys binding
            matcher: Matcher
            output_stream: Output stream
        """
        super().__init__(keys_binding=keys_binding)
        self.fullscreen = fullscreen
        self.height = height
        self.format_fn = format_fn
        self.layout: Layout = layout
        self.info_style: InfoStyle = info_style
        self.pointer_str = pointer_str
        self.no_pointer_str = " " * len(pointer_str)
        self.prompt_str = prompt_str
        self.header_str = header_str
        self.matcher = matcher() if callable(matcher) else matcher
        self.output_stream = output_stream
        # Get the candidates
        if isinstance(candidates, Iterator) or callable(candidates):
            self.get_items_fn: Union[None, Callable[[], Sequence[Any]], Iterator[Any]] = candidates
            self.candidates: Sequence[Any] = []
        else:
            self.get_items_fn = None
            self.candidates = candidates

    @property
    def screen_items(self) -> Sequence[Any]:
        "Candidates to be displayed on the screen"
        return self.matching_candidates[self.offset : self.offset + self.max_candidates_lines]

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
    def header_lines(self) -> int:
        "Number of header lines"
        return len(self.header_str.split(f"{NL}")) if self.header_str else 0

    @property
    def margin_lines(self) -> int:
        "Screen margin"
        return self.info_lines + self.prompt_lines + self.header_lines

    @property
    def max_candidates_lines(self) -> int:
        "Maximun number of candidates printables on the screen"
        return self.screen.height - self.margin_lines

    def setup(self, input: Optional[str] = None) -> None:
        """
        Setup Finder execution

        Args:
            input: initial search string
        """
        self.input = LineEditor(line=input or "", keys_handler=self.keys_handler)
        # Load the candidate list
        self.refresh_candidates()
        # Calculate the required height and setup the screen
        height = self.height if self.height is not None else self.candidates_len + self.margin_lines
        self.screen: Screen = Screen(stream=self.output_stream, fullscreen=self.fullscreen, height=height)
        # Filter the items, calculate the screen offset
        self.apply_filter()
        self.update_screen(erase=False)

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
                self.process_key()
                self.apply_filter()
                self.update_screen()
        except AcceptAction as accept:
            return accept.selected_item
        except AbortAction:
            return None
        finally:
            self.screen.cleanup()

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

    def process_key(self, ch: Optional[str] = None) -> None:
        "Process the pressed key"
        key_event = self.keys_handler.get_key_event(ch)
        try:
            self.input.process_key_event(key_event)
        except MissingHander:
            try:
                self.process_key_event(key_event)
            except MissingHander:
                raise CustomAction(action=key_event.action, ch=key_event.ch, selected_item=self.prepare_result())  # type: ignore

    def apply_filter(self) -> None:
        "Filter the items, calculate the screen offset"
        self.matching_candidates: Sequence[Any] = self.matcher.filter(
            pattern=str(self.input), candidates=self.candidates, format_fn=self.format_fn
        )
        # Adject selected
        self.selected = max(min(self.selected, self.matching_candidates_len - 1), 0)
        # Calculate the offset
        if self.selected >= self.offset + self.max_candidates_lines:
            self.offset = self.selected - self.max_candidates_lines + 1
        elif self.selected < self.offset:
            self.offset = self.selected
        if self.offset < 0:
            self.offset = 0

    def update_screen(self, erase: bool = True) -> None:
        "Update the screen - erase the old items, print the filtered items and the prompt"
        if erase:
            self.screen.erase_screen()
        if self.layout == Layout.REVERSE_LIST:
            self.print_header()
            self.print_items()
            self.print_empty_lines()
            self.print_info()
            self.print_prompt()
        self.screen.flush()

    def print_header(self) -> None:
        "Print header"
        if self.header_str:
            self.screen.erase_line().write(self.header_str).nl()

    def print_items(self) -> None:
        "Print candidates"
        for i, item in enumerate(self.screen_items):
            is_selected = i + self.offset == self.selected
            self.screen.erase_line()
            if is_selected:
                self.screen.write(f"{RED}{BOLD}{BLACK_BG}{self.pointer_str}").reset().bold()
            else:
                self.screen.write(f"{BLACK_BG}{self.no_pointer_str}").reset()
            self.screen.space(1).write(self.format_fn(item)).reset().nl()

    def print_empty_lines(self) -> None:
        "Print empty lines"
        lines = self.max_candidates_lines - self.screen_items_len
        self.screen.nl(lines)

    def print_info(self) -> None:
        "Print info"
        if self.info_style == InfoStyle.DEFAULT:
            self.screen.erase_line().space(2).write(f"{YELLOW}{self.matching_candidates_len}/{self.candidates_len}").reset().nl()

    def print_prompt(self) -> None:
        "Print prompt"
        self.screen.erase_line().write(f"{CYAN}{self.prompt_str}").reset()
        self.input.print(self.screen)

    def match(self, item: Any) -> bool:
        return str(self.input).lower() in self.format_fn(item).lower()

    def prepare_result(self) -> Any:
        "Output the selected item, if any"
        try:
            return self.matching_candidates[self.selected]
        except IndexError:
            return None

    @Action("accept", keys=["enter"])
    def accept(self, key_event: KeyEvent) -> None:
        "Confirm"
        raise AcceptAction(action="accept", ch=key_event.ch, selected_item=self.prepare_result())

    @Action("abort", keys=["ctrl-c", "ctrl-g", "ctrl-q", "esc"])
    def abort(self, key_event: KeyEvent) -> None:
        "Cancel"
        raise AbortAction(action="abort", ch=key_event.ch)

    @Action("down", keys=["ctrl-j", "ctrl-n", "down"])
    def down(self) -> None:
        "Move one line down"
        self.selected = self.selected + 1

    @Action("up", keys=["ctrl-k", "ctrl-p", "up"])
    def up(self) -> None:
        "Move one line up"
        self.selected = self.selected - 1

    @Action("page-down", keys=["page-down", "pgdn"])
    def page_down(self) -> None:
        "Move one page down"
        self.selected = self.selected + self.max_candidates_lines

    @Action("page-up", keys=["page-up", "pgup"])
    def page_up(self) -> None:
        "Move one page up"
        self.selected = self.selected - self.max_candidates_lines

    @Action("ignore", keys=["null", "insert"])
    def ignore(self) -> None:
        "Do nothing"
        pass
