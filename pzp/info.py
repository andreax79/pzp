from enum import Enum
from typing import Sequence, Union

__all__ = [
    "InfoStyle",
    "list_styles",
    "get_style",
]


class InfoStyle(Enum):
    "Display style of finder info"

    DEFAULT = "default"
    " Display on the next line to the prompt "
    HIDDEN = "hidden"
    " Do not display finder info"


def list_styles() -> Sequence[str]:
    "List styles"
    return [InfoStyle.DEFAULT.value, InfoStyle.HIDDEN.value]


def get_style(style: Union[str, InfoStyle]) -> InfoStyle:
    "Get a style by name"
    if style == InfoStyle.DEFAULT:
        return InfoStyle.DEFAULT
    elif style == InfoStyle.HIDDEN:
        return InfoStyle.HIDDEN
    else:
        return InfoStyle.DEFAULT
