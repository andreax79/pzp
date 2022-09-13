from pzp.finder import Finder
from pzp.screen import Screen
import pyte


class FakeIO:
    def __init__(self, stream):
        self.stream = stream

    def write(self, s):
        if s:
            return self.stream.feed(s.replace("\n", "\r\n"))
        else:
            return 0

    def flush(self):
        pass


class FakeTerminal:
    def __init__(self):
        self.screen = pyte.Screen(80, 24)
        self.stream = pyte.Stream(self.screen)
        self.output_stream = FakeIO(self.stream)

    @property
    def cursor(self):
        return self.screen.cursor

    def __str__(self):
        return "\n".join(self.screen.display)


def test_screen():
    terminal = FakeTerminal()
    screen = Screen(stream=terminal.output_stream, fullscreen=True, height=24)
    assert terminal.cursor.y == 0
    screen.move_down(10)
    screen.flush()
    assert terminal.cursor.y == 10
    screen.move_up(5)
    screen.flush()
    assert terminal.cursor.y == 5


def test_term():
    terminal = FakeTerminal()
    output_stream = terminal.output_stream
    assert terminal.cursor.y == 0

    lines = 4
    for i in range(0, lines):
        output_stream.write(f"line{i}>\n")
    assert terminal.cursor.y == lines

    candidates = [f"0x{x}" for x in range(0, 100)]
    finder = Finder(candidates=candidates, height=10, fullscreen=True, output_stream=output_stream)
    finder.setup()
    assert finder.selected == 0

    finder.process_key("down")
    finder.apply_filter()
    finder.update_screen()
    assert finder.selected == 1

    finder.process_key("9")
    finder.apply_filter()
    finder.update_screen()
    assert finder.selected == 1

    finder.process_key("9")
    finder.apply_filter()
    finder.update_screen()
    assert finder.selected == 0

    assert finder.prepare_result() == "0x99"
    # print(terminal)
    # assert terminal.cursor.y == finder.height + lines - 1

    finder.screen.cleanup()
    # output_stream.write("done\n")
    # print(terminal.cursor.y)
    # print("-----")
    # print(terminal)
    # print("-----")
