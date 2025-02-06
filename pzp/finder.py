#!/usr/bin/env python

import sys
from typing import Any, Callable, Iterator, Optional, Sequence, TextIO, Type, Union

from .actions import Action, ActionsHandler
from .candidates import Candidates
from .config import Config
from .exceptions import AbortAction, AcceptAction, CustomAction, MissingHander
from .info import InfoStyle
from .keys import KeyEvent, KeysBinding
from .layout import Layout, get_layout
from .line_editor import LineEditor
from .matcher import Matcher

__all__ = [
    "Finder",
    "DEFAULT_POINTER",
    "DEFAULT_PROMPT",
    "DEFAULT_HEADER",
    "DEFAULT_LAYOUT",
    "DEFAULT_MATCHER",
]

DEFAULT_POINTER = ">"
"Default pointer"
DEFAULT_PROMPT = "> "
"Default input prompt"
DEFAULT_HEADER = ""
"Default header"
DEFAULT_LAYOUT = "default"
"Default layout"
DEFAULT_MATCHER = "extended"
"Default matcher"


class Finder(ActionsHandler):
    def __init__(
        self,
        candidates: Union[Callable[[], Sequence[Any]], Iterator[Any], Sequence[Any]],
        fullscreen: bool = True,
        height: Optional[int] = None,
        format_fn: Callable[[Any], str] = lambda x: str(x),
        layout: Union[Type[Layout], str] = DEFAULT_LAYOUT,
        info_style: Union[InfoStyle, str] = InfoStyle.DEFAULT,
        pointer_str: str = DEFAULT_POINTER,
        prompt_str: str = DEFAULT_PROMPT,
        header_str: str = DEFAULT_HEADER,
        keys_binding: Optional[KeysBinding] = None,
        matcher: Union[Matcher, Type[Matcher], str] = DEFAULT_MATCHER,
        lazy: bool = False,
        output_stream: TextIO = sys.stderr,
        auto_refresh: Optional[int] = None,
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
            lazy: Lazy mode, starts the finder only if the candidates are more than one
            output_stream: Output stream
            auto_refresh: Auto refresh period (in seconds)
        """
        super().__init__(keys_binding=keys_binding)
        self.config = Config(
            fullscreen,
            height,
            format_fn,
            info_style,
            pointer_str,
            prompt_str,
            header_str,
            lazy,
            output_stream,
            auto_refresh,
        )
        self.candidates = Candidates(candidates=candidates, format_fn=format_fn, matcher=matcher)
        self.layout: Layout = get_layout(layout=layout, config=self.config, candidates=self.candidates)

    def setup(self, input: Optional[str] = None, selected: Optional[int] = None) -> None:
        """
        Setup Finder execution

        Args:
            input: initial search string
        """
        self.line_editor = LineEditor(line=input or "", keys_handler=self.keys_handler)
        # Load the candidate list
        self.refresh_candidates()
        # Filter the items, calculate the screen offset
        self.apply_filter()
        if selected is not None:
            self.selected = selected
        # If lazy mode is enabled, starts the finder only if the candidates are more than one
        if self.config.lazy and self.candidates.matching_candidates_len <= 1:
            raise AcceptAction(action="lazy-accept", ch=None, selected_item=self.prepare_result(), line=self.line_editor.line)
        # Calculate the required height and setup the screen
        self.layout.screen_setup(self.line_editor, self.selected)

    def show(self, input: Optional[str] = None) -> Any:
        """
        Open pzp and return the selected element

        Args:
            input: initial search string

        Raises:
            AcceptAction: Raises when the user presses a key that is mapped to the "accept" action.
            AbortAction: Raises when the user presses a key that is mapped to the "abort" action.
            CustomAction: Raises when the user presses a key that is mapped to the "custom" action.
        """
        try:
            self.setup(input=input)
            while True:
                self.process_key()
                self.apply_filter()
                self.update_screen()
        finally:
            self.layout.cleanup()

    def refresh_candidates(self) -> None:
        "Load/reload the candidate list"
        self.candidates.refresh_candidates()
        self.selected = 0

    def process_key(self, ch: Optional[str] = None) -> None:
        "Process the pressed key"
        key_event = self.keys_handler.get_key_event(ch, timeout=self.config.auto_refresh)
        try:
            self.line_editor.process_key_event(key_event)
        except MissingHander:
            try:
                self.process_key_event(key_event)
            except MissingHander:
                raise CustomAction(
                    action=key_event.action,  # type: ignore
                    ch=key_event.ch,
                    selected_item=self.prepare_result(),
                    line=self.line_editor.line,
                )

    def apply_filter(self) -> None:
        "Filter the items"
        if self.config.auto_refresh:
            self.candidates.refresh_candidates()
        self.candidates.apply_filter(pattern=str(self.line_editor))
        self.selected = max(min(self.selected, self.candidates.matching_candidates_len - 1), 0)

    def update_screen(self) -> None:
        "Update the screen - erase the old items, print the filtered items and the prompt"
        self.layout.update_screen(selected=self.selected)

    def prepare_result(self) -> Any:
        "Output the selected item, if any"
        try:
            return self.candidates.matching_candidates[self.selected]
        except IndexError:
            return None

    @Action("accept", keys=["enter"])
    def accept(self, key_event: KeyEvent) -> None:
        "Confirm"
        raise AcceptAction(action="accept", ch=key_event.ch, selected_item=self.prepare_result(), line=self.line_editor.line)

    @Action("abort", keys=["ctrl-c", "ctrl-g", "ctrl-q", "esc"])
    def abort(self, key_event: KeyEvent) -> None:
        "Cancel"
        raise AbortAction(action="abort", ch=key_event.ch, line=self.line_editor.line)

    @Action("down", keys=["ctrl-j", "ctrl-n", "down"])
    def down(self) -> None:
        "Move one line down"
        self.selected = self.layout.move_selection(self.selected, lines=-1)

    @Action("up", keys=["ctrl-k", "ctrl-p", "up"])
    def up(self) -> None:
        "Move one line up"
        self.selected = self.layout.move_selection(self.selected, lines=+1)

    @Action("page-down", keys=["page-down", "pgdn"])
    def page_down(self) -> None:
        "Move one page down"
        self.selected = self.layout.move_selection(self.selected, pages=-1)

    @Action("page-up", keys=["page-up", "pgup"])
    def page_up(self) -> None:
        "Move one page up"
        self.selected = self.layout.move_selection(self.selected, pages=+1)

    @Action("ignore", keys=["null", "insert"])
    def ignore(self) -> None:
        "Do nothing"
        pass
