#!/usr/bin/env python

try:
    from .input_posix import get_char
except ImportError:
    try:
        from .input_win import get_char
    except ImportError:
        raise Exception("Unsupported platform")

__all__ = ["get_char"]
