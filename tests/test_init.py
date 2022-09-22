from pzp.finder import Finder


def test_list():
    candidates = [f"0x{x}" for x in range(0, 100)]
    finder = Finder(candidates=candidates, height=25)
    finder.setup()
    assert finder.layout.screen_items_len == finder.layout.screen.height - 2
    assert finder.layout.config.info_lines == 1
    assert finder.candidates.candidates == candidates
    finder.refresh_candidates()
    assert finder.candidates.candidates == candidates


def test_range():
    candidates = range(0, 100)
    finder = Finder(candidates=candidates, height=25)
    finder.setup()
    assert finder.layout.screen_items_len == finder.layout.screen.height - 2
    assert finder.candidates.candidates == candidates
    finder.refresh_candidates()
    assert finder.candidates.candidates == candidates


def test_yield():
    def get_data():
        yield "a"
        yield "b"
        yield "c"

    finder = Finder(candidates=get_data(), height=25, fullscreen=True)
    finder.setup()
    assert finder.layout.screen_items_len == 3
    assert finder.candidates.candidates == ["a", "b", "c"]


def test_func():
    def get_data():
        return [1, 2, 3]

    finder = Finder(candidates=get_data, height=25, fullscreen=True)
    finder.setup()
    assert finder.layout.screen_items_len == 3
    assert finder.candidates.candidates == [1, 2, 3]
    finder.refresh_candidates()
    assert finder.layout.screen_items_len == 3
    assert finder.candidates.candidates == [1, 2, 3]


def test_func_yield():
    def get_data():
        yield "a"
        yield "b"
        yield "c"

    finder = Finder(candidates=get_data, height=25, fullscreen=True)
    finder.setup()
    assert finder.layout.screen_items_len == 3
    assert finder.candidates.candidates == ["a", "b", "c"]


def test_height():
    data = list(range(0, 10))
    height = 10
    finder = Finder(candidates=data, height=height, fullscreen=False)
    finder.setup()
    assert finder.layout.screen.height == height
    assert finder.layout.screen_items_len == finder.layout.screen.height - 2
