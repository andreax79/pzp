#!/usr/bin/env python

from typing import Dict, Optional, Sequence
from .input import get_char

__all__ = [
    "KEYS",
    "KeyEvent",
    "KeysHandler",
    "KeysBinding",
]

KeysBinding = Dict[str, Sequence[str]]

KEYS = {
    "ctrl-a": "\x01",
    "ctrl-b": "\x02",
    "ctrl-c": "\x03",
    "ctrl-d": "\x04",
    "ctrl-e": "\x05",
    "ctrl-f": "\x06",
    "ctrl-g": "\x07",
    "ctrl-h": "\x08",
    "ctrl-i": "\x09",
    "ctrl-j": "\x0a",
    "ctrl-k": "\x0b",
    "ctrl-l": "\x0c",
    "ctrl-m": "\x0d",
    "ctrl-n": "\x0e",
    "ctrl-o": "\x0f",
    "ctrl-p": "\x10",
    "ctrl-q": "\x11",
    "ctrl-r": "\x12",
    "ctrl-s": "\x13",
    "ctrl-t": "\x14",
    "ctrl-u": "\x15",
    "ctrl-v": "\x16",
    "ctrl-w": "\x17",
    "ctrl-x": "\x18",
    "ctrl-y": "\x19",
    "ctrl-z": "\x1a",
    "ctrl-\\": "\x1c",
    "ctrl-]": "\x1d",
    "ctrl-^": "\x1e",
    "ctrl-/": "\x1f",
    "pgup": "pgup",
    "page-up": "pgup",
    "pgdn": "pgdn",
    "page-down": "pgdn",
    "insert": "insert",
    "del": "del",
    "space": " ",
    "null": "\0",
    "up": "up",
    "down": "down",
    "right": "right",
    "left": "left",
    "home": "home",
    "end": "end",
    "nl": "\n",
    "enter": "\r",
    "tab": "\t",
    "bspace": "\x7f",
    "esc": "\x1b",
}


class KeyEvent:
    def __init__(self, ch: str, action: Optional[str]) -> None:
        """
        Key Event represents a key action on the keyboard.

        Args:
            ch: Pressed key
            action: Action

        Attributes:
            ch: Pressed key
            action: Action
        """
        self.ch = ch
        self.action = action

    def __str__(self) -> str:
        return f"<{self.ch}, {self.action or '-'}>"


class KeysHandler:
    def __init__(self, keys_binding: Optional[KeysBinding] = None) -> None:
        """
        Keys handler is a collection of bindings of keys to actions.

        Args:
            keys_binding: Custom key binding

        Attributes:
            keycodes_actions: key => action mapping
        """
        self.keycodes_actions: Dict[str, str] = {}
        if keys_binding:
            self.update(keys_binding)

    def update(self, keys_binding: KeysBinding) -> None:
        for action, keys in keys_binding.items():
            self.set_keys_binding(keys, action)

    def set_keys_binding(self, keys: Sequence[str], action: str) -> None:
        "Add a binding for one or more keys to an action"
        for key in keys:
            self.set_key_binding(key, action)

    def set_key_binding(self, key: str, action: str) -> None:
        "Add a binding for one key to an action"
        self.keycodes_actions[KEYS[key] if len(key) > 1 else key] = action

    def get_key_event(self, ch: Optional[str] = None) -> KeyEvent:
        if ch is None:
            ch = get_char()
        action = self.keycodes_actions.get(ch)
        return KeyEvent(ch=ch, action=action)
