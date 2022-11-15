pzp
==============

Pure-python fzf-inspired element picker

[![Build Status](https://github.com/andreax79/pzp/workflows/Tests/badge.svg)](https://github.com/andreax79/pzp/actions)
[![PyPI version](https://badge.fury.io/py/pzp.svg)](https://badge.fury.io/py/pzp)
[![PyPI](https://img.shields.io/pypi/pyversions/pzp.svg)](https://pypi.org/project/pzp)
[![Downloads](https://pepy.tech/badge/pzp/month)](https://pepy.tech/project/pzp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Known Vulnerabilities](https://snyk-widget.herokuapp.com/badge/pip/pzp/badge.svg)](https://snyk.io/test/github/andreax79/pzp)
[![Documentation](https://readthedocs.org/projects/pzp/badge/?version=latest)](https://pzp.readthedocs.io/en/latest/)

Requirements
-----------
* Python 3.6+

Install
-------

```
pip install pzp
```

Usage
-----

```
from pzp import pzp
pzp(['a', 'b', 'c'])
```


### Layout

The finder by default starts in fullscreen mode. You can make it start below the
cursor with [`fullscreen=False`](https://pzp.readthedocs.io/en/latest/api/module/#pzp.pzp) option.
Also, with the [`height`](https://pzp.readthedocs.io/en/latest/api/module/#pzp.pzp) argument you can limit the window height.

```python
pzp(candidates=range(0, 1000), fullscreen=False, height=20)
```

[![asciicast](https://asciinema.org/a/WtgiYfdtZjlShbeZaHuf5hWCZ.svg)](https://asciinema.org/a/WtgiYfdtZjlShbeZaHuf5hWCZ?autoplay=1)

You can choose between the following layout using the [`layout`](https://pzp.readthedocs.io/en/latest/api/module/#pzp.pzp) option.

* **default** Display from the bottom of the screen
* **reverse** Display from the top of the screen
* **reverse-list** Display from the top of the screen, prompt at the bottom

### Search syntax

The finder starts in "extended-search mode" where you can type in multiple search
terms delimited by spaces. e.g. `^music .mp3$ sbtrkt !fire`

| Token        | Match type                 | Description                          |
| ------------ | -------------------------- | ------------------------------------ |
| `t1 t2`      | tokens-match               | Items that include `t1` and `t2`     |
| `'star wars` | line-match (not-splitted)  | Items that include `star wars`       |
| `^music`     | prefix-exact-match         | Items that start with `music`        |
| `.py$`       | suffix-exact-match         | Items that end with `.py`            |
| `!fire`      | inverse-exact-match        | Items that do not include `fire`     |
| `!^music`    | inverse-prefix-exact-match | Items that do not start with `music` |
| `!.py$`      | inverse-suffix-exact-match | Items that do not end with `.py`     |

### Key/Event Bindings

[`keys_binding`](https://pzp.readthedocs.io/en/latest/api/module/#pzp.pzp) argument allows you to bind one or more keys to one action.
You can use it to customize key bindings or implementing custom behaviors.

```python
try:
    item = pzp(
        candidates=candidates,
        keys_binding={
            "custom-action": ["ctrl-o"],
            "exclamation": ["!"]
        },
    )
    print(item)
except CustomAction as action:
    print(action.action)
    print(action.selected_item)
```

#### Available Keys

| Key                   | Synonyms type         |
| --------------------- | --------------------- |
| space                 |                       |
| tab                   |                       |
| btab                  | shift-tab             |
| enter                 |                       |
| esc                   |                       |
| insert                |                       |
| del                   |                       |
| bspace                | bs                    |
| up                    |                       |
| down                  |                       |
| left                  |                       |
| right                 |                       |
| home                  |                       |
| end                   |                       |
| pgdn                  | page-down             |
| pgup                  | page-up               |
| f1 - f12              |                       |
| ctrl-/                |                       |
| ctrl-\                |                       |
| ctrl-]                |                       |
| ctrl-^                |                       |
| ctrl-a - ctrl-z       |                       |
| any single character  |                       |

#### Available Actions

A key can be bound to one of following actions or to a custom action.

| *Action**                 | *Default binding*                     |
| ------------------------- | ------------------------------------- |
| **accept**                | *enter*                               |
| **abort**                 | *ctrl-c*  *ctrl-g*  *ctrl-q*  *esc*   |
| **beginning-of-line**     | *ctrl-a*  *home*                      |
| **backward-char**         | *ctrl-b* *left*                       |
| **forward-char**          | *ctrl-f*  *right*                     |
| **end-of-line**           | *ctrl-e*  *end*                       |
| **backward-delete-char**  | *ctrl-h*  *bspace*                    |
| **delete-char**           | *del*                                 |
| **up**                    | *ctrl-k*  *ctrl-p*  *up*              |
| **down**                  | *ctrl-j*  *ctrl-n*  *down*            |
| **page-down**             | *pgdn*                                |
| **page-up**               | *pgup*                                |
| **ignore**                |                                       |

### Lazy Mode

[`lazy`](https://pzp.readthedocs.io/en/latest/api/module/#pzp.pzp) argument allows you to enable the lazy mode.
If the Lazy mode is enabled, starts the finder only if the candidates are more than one.
If there is only one match returns the only match, if there is no match returns None.

Licence
-------
MIT

Links
-----

* [fzf](https://github.com/junegunn/fzf)
* [ANSI Escape Sequences](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)
* [pyte, python terminal emulator](https://github.com/selectel/pyte)
* [Grip, GitHub Readme Instant Preview](https://github.com/joeyespo/grip)
* [Black, The Uncompromising Code Formatter](https://github.com/psf/black)
* [mkdocstrings, Automatic documentation from sources](https://github.com/mkdocstrings/mkdocstrings)
