#!/usr/bin/env python

import re
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Sequence, Type, Tuple, Union
from .commons import first_or_default

__all__ = [
    "Matcher",
    "ExactMatcher",
    "ExtendedMatcher",
    "get_matcher",
    "list_matchers",
]

SPLIT_ESCAPED_RE = re.compile(r"(?<!\\)\s+")
PREFIXES = ["!^", "!'", "^", "'", "!"]
SUFFIXES = ["$"]

matchers: Dict[str, Type["Matcher"]] = {}


class Matcher(ABC):
    def __init_subclass__(cls, option: str, **kwargs: Dict[str, Any]) -> None:
        "Register a subclass"
        super().__init_subclass__(**kwargs)
        matchers[option] = cls

    @abstractmethod
    def filter(self, pattern: str, candidates: Sequence[Any], format_fn: Callable[[Any], str] = lambda x: str(x)) -> Sequence[Any]:
        """
        Filter candidates according to the given pattern

        Args:
            pattern: Pattern
            candidates: Candidates
            format_fn: Items format function

        Returns:
            result: Filtered candidates
        """
        pass  # pragma: no cover


class ExactMatcher(Matcher, option="exact"):
    """
    Exact matcher
    """

    def filter(self, pattern: str, candidates: Sequence[Any], format_fn: Callable[[Any], str] = lambda x: str(x)) -> Sequence[Any]:
        pattern = pattern.lower()
        return [item for item in candidates if pattern in format_fn(item).lower()]


class ExtendedMatcherFilter:
    def __init__(self, term: str) -> None:
        self.prefix, self.term, self.suffix = self.split(term)
        # If a term is prefixed by !, the filter will exclude the lines that satisfy the term
        if "!" in self.prefix:
            self.exclude = True
        else:
            self.exclude = False
        if not self.term:
            self.exclude = False
            self.fn = self.always
        elif "'" in self.prefix:
            # Quoted - Check if the text contains the given term
            self.fn = self.in_match
        elif "^" in self.prefix:
            # If a term is prefixed by ^, the filter will include the lines than start with the given term
            if "$" in self.suffix:
                self.fn = self.exact_match
            else:
                self.fn = self.startswith_match
        elif "$" in self.suffix:
            # If a term is suffixed by $, the filter will include the lines than end with the given term
            self.fn = self.endswith_match
        else:
            # Check if the text contains the given term
            self.fn = self.in_match

    @classmethod
    def split(cls, term: str) -> Tuple[str, str, str]:
        "Split term in prefix, term, suffix"
        term, prefix = first_or_default([(term[len(p) :], p) for p in PREFIXES if term.startswith(p)], (term, ""))
        term, suffix = first_or_default([(term[: len(term) - len(s)], s) for s in SUFFIXES if term.endswith(s)], (term, ""))
        return prefix, term, suffix

    def __call__(self, txt: str) -> bool:
        "Evaluate the filter on the given text"
        if self.exclude:
            return not self.fn(txt)
        else:
            return self.fn(txt)

    def startswith_match(self, txt: str) -> bool:
        "True if the text startswith the given term"
        return txt.startswith(self.term)

    def endswith_match(self, txt: str) -> bool:
        "True if the text endswith the given term"
        return txt.endswith(self.term)

    def in_match(self, txt: str) -> bool:
        "True if the text contains the given term"
        return self.term in txt

    def exact_match(self, txt: str) -> bool:
        "Exact match"
        return self.term == txt

    def always(self, txt: str) -> bool:
        "Always return True"
        return True

    def __str__(self) -> str:
        return f"<{self.prefix}, {self.term}, {self.suffix}>"  # pragma: no cover


class ExtendedMatcher(Matcher, option="extended"):
    """
    Extended Matcher

    This matcher accept multiple patterns delimited by spaces, such as: term ^start end$ !not

    If patter is prefixed by a single-quote character ', it will not be splitted by spaces.

    A backslash can be prepend to a space to match a literal space character.

    A term can be prefixed by ^, or suffixed by $ to become an anchored-match term.
    Then matcher will search for the lines that start with or end with the given string.

    If a term is prefixed by !, the matcher will exclude the lines that satisfy the term from the result.
    """

    def filter(self, pattern: str, candidates: Sequence[Any], format_fn: Callable[[Any], str] = lambda x: str(x)) -> Sequence[Any]:
        # Prepare the filters
        filters = [ExtendedMatcherFilter(term) for term in self.split_pattern(pattern)]
        # Filter items
        return [item for item in candidates if self.filter_item(filters, item, format_fn)]

    def filter_item(
        self, filters: Sequence[ExtendedMatcherFilter], item: Any, format_fn: Callable[[Any], str] = lambda x: str(x)
    ) -> bool:
        txt: str = format_fn(item).lower()
        return all([filter_fn(txt) for filter_fn in filters])

    def split_pattern(self, pattern: str) -> Sequence[str]:
        "Split a pattern into terms"
        if pattern.startswith("'") or pattern.startswith("!'"):  # quote - keep spaces
            return [pattern.lower()]
        else:
            return [term.replace("\\", "") for term in SPLIT_ESCAPED_RE.split(pattern.lower()) if term]


def get_matcher(matcher: Union[Matcher, Type[Matcher], str]) -> Matcher:
    "Get a matcher instance by name or by class"
    if isinstance(matcher, Matcher):
        return matcher
    elif isinstance(matcher, str):
        return matchers[matcher]()
    else:
        return matcher()


def list_matchers() -> Sequence[str]:
    "List matchers"
    return list(matchers.keys())
