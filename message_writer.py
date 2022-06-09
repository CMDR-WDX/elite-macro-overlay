import threading
import time

from pynput.keyboard import Controller, Key
__sem = threading.Semaphore()

_keyboard = Controller()


def __writer(message: str):
    __sem.acquire(True)
    try:
        message_split = []
        message_split_len = 50
        for index in range(0, len(message), message_split_len):
            message_split.append(message[index:index+message_split_len])
        _keyboard.press(Key.enter)
        time.sleep(.1)
        _keyboard.release(Key.enter)
        time.sleep(.1)
        for msg in message_split:
            _keyboard.type(msg)
            time.sleep(.05)
        _keyboard.press(Key.enter)
        time.sleep(.1)
        _keyboard.release(Key.enter)

    finally:
        __sem.release()


def write(message: str):
    t = threading.Thread(target=__writer, args=[message])
    t.start()


