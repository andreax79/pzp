#!/usr/bin/env python

try:
    from .input_posix import get_char, KEYS_MAPPING
except ImportError:
    try:
        from .input_win import get_char, KEYS_MAPPING
    except ImportError:
        raise Exception("Unsupported platform")

__all__ = ["get_char", "KEYS_MAPPING"]
