#!/usr/bin/env python

import inspect
from typing import Any, Callable, Dict, Union
from .keys import KeyEvent
from .exceptions import MissingHander

ActionHandler = Union[Callable[[Any], None], Callable[[Any, KeyEvent], None]]

__all__ = [
    "Action",
    "ActionsHandler",
]


class Action:
    def __init__(self, action: str) -> None:
        """
        Action decorator

        Args:
            action: Action
        """
        self.action = action

    def __call__(self, func: ActionHandler) -> ActionHandler:
        setattr(func, "pzp_action", self.action)
        return func


class ActionsHandler:
    def __init__(self) -> None:
        """
        Action handler decorator

        Args:
            action: Action

        Attributes:
            actions: map action names to action handlers
        """
        self.actions: Dict[str, ActionHandler] = {}
        for name, member in inspect.getmembers(self):
            action = getattr(member, "pzp_action", None)
            if action is not None:
                self.actions[action] = member
            if name == "default":
                self.actions["default"] = member

    def process_key_event(self, key_event: KeyEvent) -> None:
        """
        Execute the action hander for a give key event

        Args:
            key_event: Key event to be processed

        Raises:
            MissingHander: If there is no handler for the given key event
        """
        action: str = key_event.action or "default"
        fn = self.actions.get(action)
        if not fn:
            raise MissingHander(action=action, ch=key_event.ch)
        if "key_event" in inspect.getargs(fn.__code__).args:
            fn(key_event=key_event)  # type: ignore
        else:
            fn()  # type: ignore
