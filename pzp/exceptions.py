#!/usr/bin/env python

from typing import Any

__all__ = [
    "PZPException",
    "GenericAction",
    "AcceptAction",
    "AbortAction",
    "CustomAction",
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
        selected_item: selected item, if any
        ch: pressed key

    Attributes:
        action: action
        selected_item: selected item, if any
        ch: pressed key

    """

    def __init__(self, action: str, selected_item: Any, ch: str):
        super().__init__(action)
        self.action = action
        self.selected_item = selected_item
        self.ch = ch


class AcceptAction(GenericAction):
    """
    The AcceptAction exception is raised when the user presses a key
    that is mapped to the "accept" action.

    Args:
        action: action
        selected_item: selected item, if any
        ch: pressed key

    Attributes:
        action: action
        selected_item: selected item, if any
        ch: pressed key

    """

    def __init__(self, action: str, selected_item: Any, ch: str):
        super().__init__(action, selected_item, ch)


class AbortAction(GenericAction):
    """
    The AbortAction exception is raised when the user presses a key
    that is mapped to the "abort" action.

    Args:
        action: action
        selected_item: selected item, if any
        ch: pressed key

    Attributes:
        action: action
        selected_item: selected item, if any
        ch: pressed key

    """

    def __init__(self, action: str, selected_item: Any, ch: str):
        super().__init__(action, selected_item, ch)


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

    def __init__(self, action: str, selected_item: Any, ch: str):
        super().__init__(action, selected_item, ch)
