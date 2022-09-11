#!/usr/bin/env python

from .finder import Finder, Layout, InfoStyle
from typing import Any, Callable, Iterator, Optional, Sequence, Union

__version__ = "0.0.2"
"PZP Version"

__all__ = ["pzp"]


def pzp(
    candidates: Union[Callable[[], Sequence[Any]], Iterator[Any], Sequence[Any]],
    max_lines: Optional[int] = None,
    format_fn: Callable[[Any], str] = lambda x: str(x),
    layout: Layout = Layout.REVERSE_LIST,
    info_style: InfoStyle = InfoStyle.DEFAULT,
    input: Optional[str] = None,
) -> Any:
    """
    Open pzp and return the selected element

    Examples:
        >>> pzp(candidates=list(Path('.').iterdir()))
        PosixPath('README.md')

    Args:
        candidates: Candidates
        max_lines: Max display lines
        format_fn: Items format function
        layout: Finder layout
        info_style: Determines the display style of finder info
        input: initial search string
    """
    finder = Finder(candidates=candidates, max_lines=max_lines, format_fn=format_fn, layout=layout, info_style=info_style)
    return finder.show(input=input)
