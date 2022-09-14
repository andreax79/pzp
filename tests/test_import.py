def test_import_module():
    import pzp

    assert pzp


def test_import_ansi():
    from pzp import ansi

    assert ansi


def test_import_exceptions():
    from pzp import exceptions

    assert exceptions


def test_import_finder():
    from pzp import finder

    assert finder


def test_import_input():
    from pzp import input

    assert input


def test_import_keys():
    from pzp import keys

    assert keys


def test_line_editor():
    from pzp import line_editor

    assert line_editor


def test_import_screen():
    from pzp import screen

    assert screen
