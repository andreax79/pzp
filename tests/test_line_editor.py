from pzp.line_editor import LineEditor


def test_line_editor():
    le = LineEditor()
    assert len(le) == 0
    assert str(le) == ""
    t = "abcdefgh"
    for c in t:
        le.insert(c)
    assert str(le) == t
    assert len(le) == len(t)
    assert le.cursor_pos == len(t)
    le.delete_char()
    assert str(le) == t
    assert len(le) == len(t)
    le.delete_backward_char()
    assert str(le) == t[:-1]
    assert len(le) == len(t) - 1
    le.beginning_of_line()
    assert le.cursor_pos == 0
    le.delete_backward_char()
    assert str(le) == t[:-1]
    assert len(le) == len(t) - 1


def test_line_editor_move():
    t = "abcdefgh"
    le = LineEditor(t)
    le.set_cursor_pos(0)
    le.forward_char()
    le.forward_char()
    assert le.cursor_pos == 2
    for _ in range(0, 10):
        le.forward_char()
    assert le.cursor_pos == len(le)
    le.backward_char()
    le.backward_char()
    assert le.cursor_pos == len(le) - 2
    for _ in range(0, 20):
        le.backward_char()
    assert le.cursor_pos == 0
    le.end_of_line()
    assert le.cursor_pos == len(le)
    le.beginning_of_line()
    assert le.cursor_pos == 0
