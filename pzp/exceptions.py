#!/usr/bin/env python

from typing import Any, Optional

__all__ = [
    "PZPException",
    "GenericAction",
    "AcceptAction",
    "AbortAction",
    "CustomAction",
    "MissingHander",
]


class PZPException(Exception):
    """
    Generic PZP Exception
    """


class GenericAction(PZPException):
    """
    Generic Action Event

    Args:
        action: action
        ch: pressed key
        selected_item: selected item, if any
        line: user input

    Attributes:
        action: action
        ch: pressed key
        selected_item: selected item, if any
        line: user input
    """

    def __init__(self, action: str, ch: Optional[str], selected_item: Any = None, line: Optional[str] = None):
        super().__init__(action)
        self.action = action
        self.ch = ch
        self.selected_item = selected_item
        self.line = line


class AcceptAction(GenericAction):
    """
    The AcceptAction exception is raised when the user presses a key
    that is mapped to the "accept" action.

    Args:
        action: action
        ch: pressed key
        selected_item: selected item, if any
        line: user input

    Attributes:
        action: action
        ch: pressed key
        selected_item: selected item, if any
        line: user input
    """

    def __init__(self, action: str, ch: Optional[str], selected_item: Any = None, line: Optional[str] = None):
        super().__init__(action, ch, selected_item, line)


class AbortAction(GenericAction):
    """
    The AbortAction exception is raised when the user presses a key
    that is mapped to the "abort" action.

    Args:
        action: action
        ch: pressed key
        selected_item: selected item, if any
        line: user input

    Attributes:
        action: action
        ch: pressed key
        selected_item: selected item, if any
        line: user input
    """

    def __init__(self, action: str, ch: Optional[str], selected_item: Any = None, line: Optional[str] = None):
        super().__init__(action, ch, selected_item, line)


class CustomAction(GenericAction):
    """
    The CustomAction exception is raised when the user presses a key
    that is mapped to the "custom" action.

    Args:
        action: action
        selected_item: selected item, if any
        ch: pressed key
        line: user input

    Attributes:
        action: action
        selected_item: selected item, if any
        ch: pressed key
        line: user input
    """

    def __init__(self, action: str, ch: Optional[str], selected_item: Any = None, line: Optional[str] = None):
        super().__init__(action, ch, selected_item, line)


class MissingHander(PZPException):
    """
    The MissingHander exception is raised when there is no handler for an action.

    Args:
        action: action
        ch: pressed key

    Attributes:
        action: action
        ch: pressed key
    """

    def __init__(self, action: str, ch: Optional[str]):
        super().__init__(action)
        self.action = action
        self.ch = ch
