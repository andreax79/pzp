#!/usr/bin/env python

from .finder import (
    Finder,
    DEFAULT_POINTER,
    DEFAULT_PROMPT,
    DEFAULT_HEADER,
    DEFAULT_LAYOUT,
    DEFAULT_MATCHER,
)
from .keys import KeysBinding
from .matcher import Matcher
from .layout import Layout
from .info import InfoStyle
from .exceptions import AcceptAction, AbortAction, CustomAction, GenericAction
from .prompt import Prompt
from typing import Any, Callable, Iterator, Optional, Sequence, Set, Type, Union

__version__ = "0.0.18"
"PZP Version"

__all__ = [
    "pzp",
    "CustomAction",
    "GenericAction",
    "Finder",
]


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
    lazy: bool = False,
    handle_actions: Set[Type[GenericAction]] = {AcceptAction, AbortAction},
    input: Optional[str] = None,
) -> Any:
    """
    Open pzp and return the selected element

    If the Lazy mode is enabled, starts the finder only if the candidates are more than one.
    If there is only one match returns the only match, if there is no match returns None.

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
        lazy: Lazy mode, starts the finder only if the candidates are more than one
        handle_actions: Actions to be handled

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
        lazy=lazy,
    )
    try:
        finder.show(input=input)
    except GenericAction as ex:
        if type(ex) in (handle_actions or set()):
            return ex.selected_item if isinstance(ex, AcceptAction) else None
        else:
            raise


def prompt(
    text: str = "",
    default: Optional[Any] = None,
    prompt_suffix: str = ": ",
    show_default: bool = True,
    input: Optional[str] = None,
) -> Any:
    """
    Ask for user input.

    Examples:
        >>> prompt("Name")
        your input

    Args:
        text: Prompt text
        default: default value to use if no input happens.
                 If this is not given it will prompt until it's aborted.
        prompt_suffix: Suffix that should be added to the prompt
        show_default: Show default value

    Returns:
        item: the selected item
    """
    if default is not None and show_default:
        prompt_str = f"{text} [{default}]{prompt_suffix}".lstrip()
    else:
        prompt_str = f"{text}{prompt_suffix}"
    prompt = Prompt(prompt_str=prompt_str)
    while True:
        try:
            prompt.show(input=input)
        except AcceptAction as ex:
            if ex.selected_item:
                return ex.selected_item
            if default is not None:
                return default
