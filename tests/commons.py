import pyte

from pzp.finder import Finder

__all__ = [
    "FakeIO",
    "FakeTerminal",
    "prepare",
]


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


def prepare(fullscreen=False, layout="default", info_style="default", candidates=None):
    terminal = FakeTerminal()
    output_stream = terminal.output_stream

    if candidates is None:
        candidates = [f"0x{x}" for x in range(0, 100)]
    finder = Finder(
        candidates=candidates, height=10, fullscreen=fullscreen, layout=layout, info_style=info_style, output_stream=output_stream
    )
    finder.setup()
    assert finder.selected == 0

    def k(ch):
        finder.process_key(ch)
        finder.apply_filter()
        finder.update_screen()

    return terminal, finder, k
