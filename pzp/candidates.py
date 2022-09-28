#!/usr/bin/env python

from typing import Any, Callable, Iterator, Sequence, Type, Union
from .matcher import Matcher, get_matcher

__all__ = [
    "Candidates",
]


class Candidates:
    def __init__(
        self,
        candidates: Union[Callable[[], Sequence[Any]], Iterator[Any], Sequence[Any]],
        format_fn: Callable[[Any], str],
        matcher: Union[Matcher, Type[Matcher], str],
    ):
        """
        Candidates

        Args:
            candidates: Candidates
            format_fn: Items format function
            matcher: Matcher

        Attributes:
            format_fn: Items format function
            matcher: Matcher
            candidates: candidates
            matching_candidates_len: filtered items
        """
        self.format_fn = format_fn
        self.matcher = get_matcher(matcher)
        # Get the candidates
        if isinstance(candidates, Iterator) or callable(candidates):
            self.get_items_fn: Union[None, Callable[[], Sequence[Any]], Iterator[Any]] = candidates
            self.candidates: Sequence[Any] = []
        else:
            self.get_items_fn = None
            self.candidates = candidates

    @property
    def candidates_len(self) -> int:
        "Number of candidates"
        return len(self.candidates)

    @property
    def matching_candidates_len(self) -> int:
        "Number of matching candidates"
        return len(self.matching_candidates)

    def refresh_candidates(self) -> None:
        "Load/reload the candidate list"
        # Get items
        if isinstance(self.get_items_fn, Iterator):
            self.candidates = list(self.get_items_fn)
        elif callable(self.get_items_fn):
            self.candidates = list(self.get_items_fn())

    def apply_filter(self, pattern: str) -> None:
        "Filter the items"
        self.matching_candidates: Sequence[Any] = self.matcher.filter(
            pattern=pattern, candidates=self.candidates, format_fn=self.format_fn
        )
