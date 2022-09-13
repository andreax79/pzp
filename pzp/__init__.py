#!/usr/bin/env python

from .finder import Finder, Layout, InfoStyle, DEFAULT_POINTER, DEFAULT_PROMPT
from typing import Any, Callable, Iterator, Optional, Sequence, Union

__version__ = "0.0.5"
"PZP Version"

__all__ = ["pzp"]


def pzp(
    candidates: Union[Callable[[], Sequence[Any]], Iterator[Any], Sequence[Any]],
    height: Optional[int] = None,
    fullscreen: bool = True,
    format_fn: Callable[[Any], str] = lambda x: str(x),
    layout: Layout = Layout.REVERSE_LIST,
    info_style: InfoStyle = InfoStyle.DEFAULT,
    pointer_str: str = DEFAULT_POINTER,
    prompt_str: str = DEFAULT_PROMPT,
    input: Optional[str] = None,
) -> Any:
    """
    Open pzp and return the selected element

    Examples:
        >>> pzp(candidates=list(Path('.').iterdir()))
        PosixPath('README.md')

    Args:
        candidates: Candidates
        fullscreen: Full screen mode
        height: Finder window height
        format_fn: Items format function
        layout: Finder layout
        info_style: Determines the display style of finder info
        pointer_str: Pointer to the current line
        prompt_str: Input prompt

    Returns:
        item: the selected item
    """
    finder = Finder(
        candidates=candidates,
        fullscreen=fullscreen,
        height=height,
        format_fn=format_fn,
        layout=layout,
        info_style=info_style,
        pointer_str=pointer_str,
        prompt_str=prompt_str,
    )
    return finder.show(input=input)
