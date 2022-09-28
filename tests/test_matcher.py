from pathlib import Path
from pzp.finder import Finder
from pzp.matcher import ExactMatcher, ExtendedMatcher, ExtendedMatcherFilter

tests_dir = Path(__file__).parent
code_of_conduct = tests_dir.parent / "CODE_OF_CONDUCT.md"


class LineItem:
    def __init__(self, i, line):
        self.i = i
        self.line = line

    def __str__(self):
        return self.line


def test_extended_matcher_filter():
    t = ExtendedMatcherFilter("")
    assert t.prefix == "" and t.suffix == "" and t.term == ""
    t = ExtendedMatcherFilter("aaa")
    assert t.prefix == "" and t.suffix == "" and t.term == "aaa"
    t = ExtendedMatcherFilter("!aaa")
    assert t.prefix == "!" and t.suffix == "" and t.term == "aaa"
    t = ExtendedMatcherFilter("!'aaa")
    assert t.prefix == "!'" and t.suffix == "" and t.term == "aaa"
    t = ExtendedMatcherFilter("^aaa")
    assert t.prefix == "^" and t.suffix == "" and t.term == "aaa"
    t = ExtendedMatcherFilter("!^aaa")
    assert t.prefix == "!^" and t.suffix == "" and t.term == "aaa"
    t = ExtendedMatcherFilter("^aaa$")
    assert t.prefix == "^" and t.suffix == "$" and t.term == "aaa"
    t = ExtendedMatcherFilter("!^aaa$")
    assert t.prefix == "!^" and t.suffix == "$" and t.term == "aaa"
    t = ExtendedMatcherFilter("!aaa$")
    assert t.prefix == "!" and t.suffix == "$" and t.term == "aaa"
    t = ExtendedMatcherFilter("aaa$")
    assert t.prefix == "" and t.suffix == "$" and t.term == "aaa"


def test_matcher_in():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.line_editor.line = ""
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == len(finder.candidates.candidates)

    finder.line_editor.line = "ex"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 13
    assert all(["ex" in item.lower() for item in finder.candidates.matching_candidates])

    finder.line_editor.line = "ex e"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 13
    assert all(["ex" in item.lower() for item in finder.candidates.matching_candidates])

    finder.line_editor.line = "ex ex"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 13
    assert all(["ex" in item.lower() for item in finder.candidates.matching_candidates])


def test_matcher_not_in():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.line_editor.line = "!ex"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == len(candidates) - 13
    assert all(["ex" not in item.lower() for item in finder.candidates.matching_candidates])

    finder.line_editor.line = "!ex ex"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 0

    finder.line_editor.line = "!ex We"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 7
    assert all(["ex" not in item.lower() for item in finder.candidates.matching_candidates])
    assert all(["we" in item.lower() for item in finder.candidates.matching_candidates])

    finder.line_editor.line = "!"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == len(candidates)


def test_matcher_startswith():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.line_editor.line = "^We"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 2

    finder.line_editor.line = "^We as"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 1

    finder.line_editor.line = "as ^We"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 1

    finder.line_editor.line = "as ^bla"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 0


def test_matcher_not_startswith():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.line_editor.line = "!^We"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == len(candidates) - 2

    finder.line_editor.line = "!^We as"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 12

    finder.line_editor.line = "as !^We"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 12

    finder.line_editor.line = "!^bla"
    finder.apply_filter()


def test_matcher_endswith():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.line_editor.line = ",$"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 6

    finder.line_editor.line = "s,$"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 3

    finder.line_editor.line = "* s,$"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 1


def test_matcher_not_endswith():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.line_editor.line = "!,$"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == len(candidates) - 6

    finder.line_editor.line = "!s,$"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == len(candidates) - 3

    finder.line_editor.line = "* !s,$"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 17


def test_quoted():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.line_editor.line = "'  "
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 6

    finder.line_editor.line = "'to this"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 1

    finder.line_editor.line = "!'to this"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == len(candidates) - 1


def test_line_exact_match():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.line_editor.line = "^##\\ Scope$"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 1


def test_exact_matcher():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True, matcher=ExactMatcher)
    finder.setup()

    finder.line_editor.line = "  "
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 6

    finder.line_editor.line = "to this"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 1

    finder.line_editor.line = "!'to this"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 0


def test_extended_matcher():
    matcher = ExtendedMatcher()
    candidates = range(0, 1000)
    result = matcher.filter("0", candidates)
    assert len(result) == 181
    result = matcher.filter("9", candidates)
    assert len(result) == 271
    result = matcher.filter("0 1", candidates)
    assert len(result) == 36
    result = matcher.filter("0 !1", candidates)
    assert len(result) == 181 - 36
    result = matcher.filter("!^0", candidates)
    assert len(result) == 999


def test_matcher_format_fn():
    candidates = [LineItem(i, line) for i, line in enumerate(code_of_conduct.read_text().split("\n"), start=1)]
    finder = Finder(
        candidates=candidates,
        height=10,
        fullscreen=True,
        format_fn=lambda item: f"{item.i:3d}: {item.line}",
    )
    finder.setup()

    finder.line_editor.line = "ex"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 13
    assert all(["ex" in item.line.lower() for item in finder.candidates.matching_candidates])

    finder.line_editor.line = "20:"
    finder.apply_filter()
    assert len(finder.candidates.matching_candidates) == 2
    assert all(["20" in str(x.i) for x in finder.candidates.matching_candidates])
