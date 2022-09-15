#!/usr/bin/env python

from typing import Any

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

    Attributes:
        action: action
        ch: pressed key
        selected_item: selected item, if any
    """

    def __init__(self, action: str, ch: str, selected_item: Any = None):
        super().__init__(action)
        self.action = action
        self.ch = ch
        self.selected_item = selected_item


class AcceptAction(GenericAction):
    """
    The AcceptAction exception is raised when the user presses a key
    that is mapped to the "accept" action.

    Args:
        action: action
        ch: pressed key
        selected_item: selected item, if any

    Attributes:
        action: action
        ch: pressed key
        selected_item: selected item, if any
    """

    def __init__(self, action: str, ch: str, selected_item: Any = None):
        super().__init__(action, ch, selected_item)


class AbortAction(GenericAction):
    """
    The AbortAction exception is raised when the user presses a key
    that is mapped to the "abort" action.

    Args:
        action: action
        ch: pressed key
        selected_item: selected item, if any

    Attributes:
        action: action
        ch: pressed key
        selected_item: selected item, if any
    """

    def __init__(self, action: str, ch: str, selected_item: Any = None):
        super().__init__(action, ch, selected_item)


class CustomAction(GenericAction):
    """
    The CustomAction exception is raised when the user presses a key
    that is mapped to the "custom" action.

    Args:
        action: action
        selected_item: selected item, if any
        ch: pressed key

    Attributes:
        action: action
        selected_item: selected item, if any
        ch: pressed key
    """

    def __init__(self, action: str, ch: str, selected_item: Any = None):
        super().__init__(action, ch, selected_item)


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

    def __init__(self, action: str, ch: str):
        super().__init__(action)
        self.action = action
        self.ch = ch
