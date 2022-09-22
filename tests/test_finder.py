import pytest
from pzp.finder import Finder
from pzp.keys import KEYS
from pzp.exceptions import AcceptAction, AbortAction, CustomAction


def test_actions():
    candidates = [f"0x{x}" for x in range(0, 100)]
    finder = Finder(
        candidates=candidates,
        height=10,
        fullscreen=True,
        layout="reverse-list",
        keys_binding={"custom": ["ctrl-o"], "ignore": ["ctrl-i"]},
    )
    finder.setup()
    assert finder.selected == 0

    finder.process_key("down")
    finder.apply_filter()
    finder.update_screen()
    assert finder.selected == 1

    finder.process_key(KEYS["pgup"])
    finder.apply_filter()
    assert finder.selected == 0

    finder.process_key(KEYS["pgdn"])
    finder.apply_filter()
    assert finder.selected == 22

    finder.process_key("up")
    finder.apply_filter()
    assert finder.selected == 21

    finder.process_key(KEYS["pgup"])
    finder.apply_filter()
    assert finder.selected == 0

    finder.process_key(KEYS["ctrl-a"])
    finder.process_key(KEYS["ctrl-b"])
    finder.process_key(KEYS["ctrl-i"])
    with pytest.raises(CustomAction):
        finder.process_key(KEYS["ctrl-o"])
    with pytest.raises(AbortAction):
        finder.process_key(KEYS["ctrl-c"])
    with pytest.raises(AcceptAction) as except_info:
        finder.process_key(KEYS["enter"])
    assert except_info.value.action == "accept"
    assert except_info.value.ch == KEYS["enter"]
    assert except_info.value.selected_item == "0x0"
