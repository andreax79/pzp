from pathlib import Path
from pzp.finder import Finder
from pzp.matcher import ExactMatcher, ExtendedMatcher, ExtendedMatcherFilter

tests_dir = Path(__file__).parent
code_of_conduct = tests_dir.parent / "CODE_OF_CONDUCT.md"


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

    finder.input.line = ""
    finder.apply_filter()
    assert len(finder.matching_candidates) == len(finder.candidates)

    finder.input.line = "ex"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 13
    assert all(["ex" in item.lower() for item in finder.matching_candidates])

    finder.input.line = "ex e"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 13
    assert all(["ex" in item.lower() for item in finder.matching_candidates])

    finder.input.line = "ex ex"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 13
    assert all(["ex" in item.lower() for item in finder.matching_candidates])


def test_matcher_not_in():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.input.line = "!ex"
    finder.apply_filter()
    assert len(finder.matching_candidates) == len(candidates) - 13
    assert all(["ex" not in item.lower() for item in finder.matching_candidates])

    finder.input.line = "!ex ex"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 0

    finder.input.line = "!ex We"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 7
    assert all(["ex" not in item.lower() for item in finder.matching_candidates])
    assert all(["we" in item.lower() for item in finder.matching_candidates])

    finder.input.line = "!"
    finder.apply_filter()
    assert len(finder.matching_candidates) == len(candidates)


def test_matcher_startswith():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.input.line = "^We"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 2

    finder.input.line = "^We as"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 1

    finder.input.line = "as ^We"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 1

    finder.input.line = "as ^bla"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 0


def test_matcher_not_startswith():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.input.line = "!^We"
    finder.apply_filter()
    assert len(finder.matching_candidates) == len(candidates) - 2

    finder.input.line = "!^We as"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 12

    finder.input.line = "as !^We"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 12

    finder.input.line = "!^bla"
    finder.apply_filter()


def test_matcher_endswith():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.input.line = ",$"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 6

    finder.input.line = "s,$"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 3

    finder.input.line = "* s,$"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 1


def test_matcher_not_endswith():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.input.line = "!,$"
    finder.apply_filter()
    assert len(finder.matching_candidates) == len(candidates) - 6

    finder.input.line = "!s,$"
    finder.apply_filter()
    assert len(finder.matching_candidates) == len(candidates) - 3

    finder.input.line = "* !s,$"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 17


def test_quoted():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.input.line = "'  "
    finder.apply_filter()
    assert len(finder.matching_candidates) == 6

    finder.input.line = "'to this"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 1

    finder.input.line = "!'to this"
    finder.apply_filter()
    assert len(finder.matching_candidates) == len(candidates) - 1


def test_line_exact_match():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True)
    finder.setup()

    finder.input.line = "^##\\ Scope$"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 1


def test_exact_matcher():
    candidates = code_of_conduct.read_text().split("\n")
    finder = Finder(candidates=candidates, height=10, fullscreen=True, matcher=ExactMatcher)
    finder.setup()

    finder.input.line = "  "
    finder.apply_filter()
    assert len(finder.matching_candidates) == 6

    finder.input.line = "to this"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 1

    finder.input.line = "!'to this"
    finder.apply_filter()
    assert len(finder.matching_candidates) == 0


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
