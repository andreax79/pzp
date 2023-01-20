#!/usr/bin/env python

import sys
from typing import Any, Optional, TextIO
from .actions import Action, ActionsHandler
from .exceptions import AcceptAction, AbortAction, CustomAction, MissingHander
from .keys import KeyEvent, KeysBinding
from .line_editor import LineEditor
from .screen import Screen

__all__ = [
    "Prompt",
]


class Prompt(ActionsHandler):
    def __init__(
        self,
        prompt_str: str = "",
        keys_binding: Optional[KeysBinding] = None,
        output_stream: TextIO = sys.stderr,
    ):
        """
        Initializate Prompt object

        Args:
            prompt_str: Input prompt
            keys_binding: Custom keys binding
            output_stream: Output stream
        """
        super().__init__(keys_binding=keys_binding)
        self.prompt_str = prompt_str
        self.output_stream = output_stream

    def setup(self, input: Optional[str] = None) -> None:
        """
        Setup Prompt execution

        Args:
            input: initial string
        """
        self.line_editor = LineEditor(line=input or "", keys_handler=self.keys_handler)
        self.screen = Screen(stream=self.output_stream, fullscreen=False)
        self.update_screen()

    def show(self, input: Optional[str] = None) -> Any:
        """
        Open pzp and return the selected element

        Args:
            input: initial string

        Raises:
            AcceptAction: Raises when the user presses a key that is mapped to the "accept" action.
            AbortAction: Raises when the user presses a key that is mapped to the "abort" action.
            CustomAction: Raises when the user presses a key that is mapped to the "custom" action.
        """
        self.setup(input=input)
        while True:
            self.process_key()
            self.update_screen()

    def process_key(self, ch: Optional[str] = None) -> None:
        "Process the pressed key"
        key_event = self.keys_handler.get_key_event(ch)
        try:
            self.line_editor.process_key_event(key_event)
        except MissingHander:
            try:
                self.process_key_event(key_event)
            except MissingHander:
                raise CustomAction(action=key_event.action, ch=key_event.ch, selected_item=self.prepare_result())  # type: ignore

    def update_screen(self) -> None:
        "Update the screen"
        self.screen.write("\r").erase_line()
        self.screen.erase_line().write(self.prompt_str).reset()
        self.line_editor.print(self.screen)
        self.screen.flush()

    def prepare_result(self) -> str:
        return self.line_editor.line

    @Action("accept", keys=["enter"])
    def accept(self, key_event: KeyEvent) -> None:
        "Confirm"
        raise AcceptAction(action="accept", ch=key_event.ch, selected_item=self.prepare_result())

    @Action("abort", keys=["ctrl-c", "ctrl-g", "ctrl-q", "esc"])
    def abort(self, key_event: KeyEvent) -> None:
        "Cancel"
        raise AbortAction(action="abort", ch=key_event.ch)

    @Action("ignore", keys=["null", "insert"])
    def ignore(self) -> None:
        "Do nothing"
        pass
