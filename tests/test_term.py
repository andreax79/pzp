import pytest
from pzp import pzp
from pzp.screen import Screen
from pzp.exceptions import AcceptAction
from .commons import FakeTerminal


def test_screen_movements():
    terminal = FakeTerminal()
    screen = Screen(stream=terminal.output_stream, fullscreen=True, height=24)
    assert terminal.cursor.y == 0
    screen.move_down(10)
    screen.flush()
    assert terminal.cursor.y == 10
    screen.move_up(5)
    screen.flush()
    assert terminal.cursor.y == 5
    screen.move_right(0)
    screen.flush()
    assert terminal.cursor.x == 0
    screen.move_right(10)
    screen.flush()
    assert terminal.cursor.x == 10
    screen.move_right(100)
    screen.flush()
    assert terminal.cursor.x == 79
    screen.move_left(0)
    screen.flush()
    assert terminal.cursor.x == 79
    screen.move_left(20)
    screen.flush()
    assert terminal.cursor.x == 59
    screen.move_left(200)
    screen.flush()
    assert terminal.cursor.x == 0


def test_screen():
    terminal = FakeTerminal()
    screen = Screen(stream=terminal.output_stream, fullscreen=True, height=24)
    assert terminal.cursor.x == 0
    assert terminal.cursor.y == 0
    screen.space(10).flush()
    assert terminal.cursor.x == 10
    assert terminal.cursor.y == 0
    screen.nl(10).flush()
    assert terminal.cursor.x == 0
    assert terminal.cursor.y == 10
    screen.space().flush()
    assert terminal.cursor.x == 1
    assert terminal.cursor.y == 10
    screen.nl().flush()
    assert terminal.cursor.x == 0
    assert terminal.cursor.y == 11
    screen.space(10).erase_line().flush()
    assert terminal.cursor.x == 10


def test_term():
    terminal = FakeTerminal()
    output_stream = terminal.output_stream
    assert terminal.cursor.y == 0

    lines = 4
    for i in range(0, lines):
        output_stream.write(f"line{i}>\n")
    assert terminal.cursor.y == lines


@pytest.mark.timeout(5)
def test_lazy():
    assert pzp([1], lazy=True) == 1
    assert pzp([], lazy=True) is None
    assert pzp(["a", "b", "c"], input="a", lazy=True) == "a"
    assert pzp(["a", "b", "c"], input="d", lazy=True) is None

    with pytest.raises(AcceptAction) as ex:
        pzp(["a", "b", "c"], input="a", lazy=True, handle_actions=None)
    assert ex.value.selected_item == "a"

    with pytest.raises(AcceptAction) as ex:
        pzp(["a", "b", "c"], input="d", lazy=True, handle_actions=None)
    assert ex.value.selected_item is None
