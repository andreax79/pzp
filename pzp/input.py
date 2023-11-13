#!/usr/bin/env python

try:
    from .input_posix import KEYS_MAPPING, get_char
except ImportError:
    try:
        from .input_win import KEYS_MAPPING, get_char
    except ImportError:
        raise Exception("Unsupported platform")

__all__ = ["get_char", "KEYS_MAPPING"]
