import typing

from pynput import keyboard

__listeners: list[typing.Callable[[int], None]] = []

__keycode_lookup = dict()


def __is_numpad(vk: int):
    return 96 <= vk <= 105


def __get_numpad_value(vk: int):
    return vk - 96


def add_listener(cb):
    __listeners.append(cb)


def __on_press(key):
    if not hasattr(key, "vk"):
        return
    if key.vk is None:
        return

    if __is_numpad(key.vk):
        value = __get_numpad_value(key.vk)
        for listener in __listeners:
            listener(value)


__kb_listener = keyboard.Listener(on_press=__on_press)


def init():
    __kb_listener.start()
