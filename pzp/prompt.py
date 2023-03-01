#!/usr/bin/env python

import sys
from typing import Any, Callable, Optional, TextIO
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
        default: Optional[Any] = None,
        prompt_str: str = "",
        type: Optional[Any] = None,
        value_proc: Optional[Callable[[str], Any]] = None,
        keys_binding: Optional[KeysBinding] = None,
        output_stream: TextIO = sys.stderr,
    ):
        """
        Initializate Prompt object

        Args:
            default: The default value to use if no input happens
            prompt_str: The input prompt
            type: The type to use to check the value against
            value_proc: Type conversion function
            keys_binding: Custom keys binding
            output_stream: Output stream
        """
        super().__init__(keys_binding=keys_binding)
        self.default = default
        self.prompt_str = prompt_str
        self.output_stream = output_stream
        if value_proc is not None:
            self.value_proc: Optional[Callable[[str], Any]] = value_proc
        elif (type is not None) or (default is not None and not isinstance(default, str)):
            from click.types import convert_type

            self.value_proc = convert_type(type, default)
        else:
            self.value_proc = None

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
                raise CustomAction(action=key_event.action, ch=key_event.ch, selected_item=self.prepare_result(), line=self.line_editor.line)  # type: ignore

    def update_screen(self) -> None:
        "Update the screen"
        self.screen.write("\r").erase_line()
        self.screen.erase_line().write(self.prompt_str).reset()
        self.line_editor.print(self.screen)
        self.screen.flush()

    def prepare_result(self) -> Any:
        "Return the line converted to the correct type or the default value if the line is empty"
        if not self.line_editor.line:
            return self.default
        elif self.value_proc is not None:
            # value_proc raises an exception if the value is invalid
            return self.value_proc(self.line_editor.line)
        else:
            return self.line_editor.line

    @Action("accept", keys=["enter"])
    def accept(self, key_event: KeyEvent) -> None:
        "Confirm"
        try:
            selected_item = self.prepare_result()
        except Exception as ex:
            self.screen.write(f"\nError: The value you entered was invalid: {ex}\n")
            self.screen.flush()
            return
        raise AcceptAction(action="accept", ch=key_event.ch, selected_item=selected_item, line=self.line_editor.line)

    @Action("abort", keys=["ctrl-c", "ctrl-g", "ctrl-q", "esc"])
    def abort(self, key_event: KeyEvent) -> None:
        "Cancel"
        raise AbortAction(action="abort", ch=key_event.ch, line=self.line_editor.line)

    @Action("ignore", keys=["null", "insert"])
    def ignore(self) -> None:
        "Do nothing"
        pass
