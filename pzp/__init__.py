#!/usr/bin/env python

from .finder import CustomAction, Finder, DEFAULT_POINTER, DEFAULT_PROMPT, DEFAULT_HEADER, DEFAULT_LAYOUT, DEFAULT_MATCHER
from .keys import KeysBinding
from .matcher import Matcher
from .layout import Layout
from .info import InfoStyle
from typing import Any, Callable, Iterator, Optional, Sequence, Type, Union

__version__ = "0.0.14"
"PZP Version"

__all__ = ["pzp", "CustomAction"]


def pzp(
    candidates: Union[Callable[[], Sequence[Any]], Iterator[Any], Sequence[Any]],
    height: Optional[int] = None,
    fullscreen: bool = True,
    format_fn: Callable[[Any], str] = lambda x: str(x),
    layout: Union[Type[Layout], str] = DEFAULT_LAYOUT,
    info_style: InfoStyle = InfoStyle.DEFAULT,
    pointer_str: str = DEFAULT_POINTER,
    prompt_str: str = DEFAULT_PROMPT,
    header_str: str = DEFAULT_HEADER,
    keys_binding: Optional[KeysBinding] = None,
    matcher: Union[Matcher, Type[Matcher], str] = DEFAULT_MATCHER,
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
        header_str: Header
        keys_binding: Custom keys binding
        matcher: Matcher

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
        header_str=header_str,
        keys_binding=keys_binding,
        matcher=matcher,
    )
    return finder.show(input=input)
