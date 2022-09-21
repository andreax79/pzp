from pzp.keys import key_to_str, KeysHandler


def test_key_to_str():
    t = key_to_str("a")
    assert t == "0x61"
    t = key_to_str("ctrl-o")
    assert t == "ctrl-o"


def test_keys_handler():
    keys_binding = {"custom": ["ctrl-o"], "qu-qu": ["ctrl-q"], "oh-oh": ["!"]}
    h = KeysHandler(keys_binding)
    ev = h.get_key_event("\x0f")
    assert ev.ch == "\x0f"
    assert ev.action == "custom"
    ev = h.get_key_event("a")
    assert ev.ch == "a"
    assert ev.action is None


def test_default_keys_handler():
    h = KeysHandler()
    ev = h.get_key_event("!")
    assert ev.ch == "!"
    assert ev.action is None
    h.set_keys_binding(["!", "$"], "custom")
    ev = h.get_key_event("!")
    assert ev.ch == "!"
    assert ev.action == "custom"
    ev = h.get_key_event("$")
    assert ev.ch == "$"
    assert ev.action == "custom"
