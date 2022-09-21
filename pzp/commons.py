#!/usr/bin/env python

from typing import Sequence, TypeVar

T = TypeVar("T")

__all__ = ['first_or_default']


def first_or_default(sequence: Sequence[T], default: T) -> T:
    return sequence[0] if sequence else default
