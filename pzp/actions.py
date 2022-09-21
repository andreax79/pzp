#!/usr/bin/env python

import inspect
from typing import Any, Callable, Dict, Optional, Sequence, Union
from .keys import KeyEvent, KeysHandler, KeysBinding
from .exceptions import MissingHander

__all__ = [
    "Action",
    "ActionsHandler",
]

ActionHandler = Union[Callable[[Any], None], Callable[[Any, KeyEvent], None]]


class Action:
    def __init__(self, action: str, keys: Optional[Sequence[str]] = None) -> None:
        """
        Action decorator

        Args:
            action: Action
        """
        self.action: str = action
        self.keys: Sequence[str] = keys or []

    def __call__(self, func: ActionHandler) -> ActionHandler:
        setattr(func, "pzp_action", self.action)
        setattr(func, "pzp_keys", self.keys)
        return func


class ActionsHandler:
    def __init__(
        self,
        keys_handler: Optional[KeysHandler] = None,
        keys_binding: Optional[KeysBinding] = None,
    ) -> None:
        """
        Action handler

        Args:
            keys_handler: Keys handler
            keys_binding: Optional[Dict[str, Sequence[str]]] = None,

        Attributes:
            actions: map action names to action handlers
            keys_handler: Keys handler
        """
        self.keys_handler = keys_handler or KeysHandler()
        # Collect the methods with the Action decorator
        self.actions: Dict[str, ActionHandler] = {}
        for name, member in inspect.getmembers(self):
            action: Optional[str] = getattr(member, "pzp_action", None)
            if action is not None:
                self.actions[action] = member
                # Default action
                if name == "default":
                    self.actions["default"] = member
                # Keys binding
                keys: Optional[Sequence[str]] = getattr(member, "pzp_keys", None)
                if keys:
                    self.keys_handler.set_keys_binding(keys, action)
        # Override keys binding
        if keys_binding:
            self.keys_handler.update(keys_binding)

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
        # Check if the function has the key_event argument
        if "key_event" in inspect.getargs(fn.__code__).args:
            fn(key_event=key_event)  # type: ignore
        else:
            fn()  # type: ignore
