from .commons import prepare


def test_term_reverse_list_fullscreen():
    terminal, finder, k = prepare(fullscreen=True, layout="reverse-list")

    k("down")
    assert finder.selected == 1
    assert terminal.cursor.y == 23

    k("9")
    assert finder.selected == 1
    assert terminal.cursor.y == 23

    k("9")
    assert finder.selected == 0
    assert finder.prepare_result() == "0x99"
    assert terminal.cursor.y == 23

    k("x")
    assert finder.selected == 0
    assert finder.prepare_result() is None
    assert terminal.cursor.y == 23

    finder.layout.screen.cleanup()
    assert terminal.cursor.y == 0


def test_term_reverse_list_hidden():
    terminal, finder, k = prepare(fullscreen=False, layout="reverse-list", candidates=["Yes", "No"], info_style="hidden")
    output_stream = terminal.output_stream
    lines = 10
    for i in range(0, lines):
        output_stream.write(f"line{i}>\n")
    assert terminal.cursor.y == lines + 9

    k("down")
    assert finder.selected == 1
    assert terminal.cursor.y == lines + 9

    k("Y")
    assert finder.selected == 0
    assert terminal.cursor.y == lines + 9

    k("e")
    assert finder.selected == 0
    assert finder.prepare_result() == "Yes"
    assert terminal.cursor.y == lines + 9

    k("X")
    assert finder.selected == 0
    assert finder.prepare_result() is None
    assert terminal.cursor.y == lines + 9


def test_term_reverse_fullscreen():
    terminal, finder, k = prepare(fullscreen=True, layout="reverse")

    k("down")
    assert finder.selected == 1
    assert terminal.cursor.y == 0

    k("9")
    assert finder.selected == 1
    assert terminal.cursor.y == 0

    k("9")
    assert finder.selected == 0
    assert finder.prepare_result() == "0x99"
    assert terminal.cursor.y == 0

    k("x")
    assert finder.selected == 0
    assert finder.prepare_result() is None
    assert terminal.cursor.y == 0

    finder.layout.screen.cleanup()
    assert terminal.cursor.y == 0


def test_term_reverse():
    terminal, finder, k = prepare(fullscreen=False, layout="reverse", candidates=["Yes", "No"])
    output_stream = terminal.output_stream
    lines = 10
    for i in range(0, lines):
        output_stream.write(f"line{i}>\n")
    assert terminal.cursor.y == lines

    k("down")
    assert finder.selected == 1
    assert terminal.cursor.y == lines

    k("Y")
    assert finder.selected == 0
    assert terminal.cursor.y == lines

    k("e")
    assert finder.selected == 0
    assert finder.prepare_result() == "Yes"
    assert terminal.cursor.y == lines

    k("X")
    assert finder.selected == 0
    assert finder.prepare_result() is None
    assert terminal.cursor.y == lines


def test_term_reverse_hidden():
    terminal, finder, k = prepare(fullscreen=False, layout="reverse", candidates=["Yes", "No"], info_style="hidden")
    output_stream = terminal.output_stream
    lines = 10
    for i in range(0, lines):
        output_stream.write(f"line{i}>\n")
    assert terminal.cursor.y == lines

    k("down")
    assert finder.selected == 1
    assert terminal.cursor.y == lines

    k("Y")
    assert finder.selected == 0
    assert terminal.cursor.y == lines

    k("e")
    assert finder.selected == 0
    assert finder.prepare_result() == "Yes"
    assert terminal.cursor.y == lines

    k("X")
    assert finder.selected == 0
    assert finder.prepare_result() is None
    assert terminal.cursor.y == lines
