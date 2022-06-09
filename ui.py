import threading
import tkinter as tk
from typing import Callable
from datetime import timedelta
from datetime import datetime
import time


class UiHider:
    def __init__(self, seconds: int, notify_about_hiding: Callable):
        self.delay = timedelta(seconds=seconds)
        self.threadId = 0
        self._time_when_to_hide = datetime.now() + self.delay
        self.running = False
        self.thread = None
        self._cb = notify_about_hiding

    def notify_about_explicit_hide(self):
        self.running = False

    def notify_about_action(self):
        self._time_when_to_hide = datetime.now() + self.delay
        if not self.running:
            self.threadId += 1
            self.thread = threading.Thread(target=self.__ui_loop, daemon=True, args=[self.threadId])
            self.thread.start()

    def __ui_loop(self, id: int):
        print("Starting UI Loop "+str(id))
        self.running = True
        while self.running and self.threadId == id:
            # Sleep a second
            time.sleep(1)
            if datetime.now() > self._time_when_to_hide:
                self.running = False
                if self.threadId == id:
                    self._cb()
        print("Killing UI Loop "+str(id))



def _make_overlay(frame: tk.Tk):
    """
    Creates an overlay frame. This code has been taken from
    https://github.com/notatallshaw/fall_guys_ping_estimate/blob/296ce8207ce8b8f4240d29fbb422d7df0710bcfa/fgpe/overlay.py
    :param frame: The Frame to create an Overlay from
    """
    frame.overrideredirect(True)
    frame.config(background="white")
    frame.geometry("+20+20")
    frame.wm_attributes("-topmost", True)
    frame.wm_attributes("-transparentcolor", "white")


class UIOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.current_node = None
        _make_overlay(self.root)
        self.visible = True
        self.ui_hider = UiHider(5, self._hide_ui_callback)
        self.root.bind("<<RefreshVisibility>>", lambda _: self.notify_about_visibility_switch())
        self.reset_tree_callback = []

    def _hide_ui_callback(self):
        """
        Called from Thread
        """
        self.visible = True
        self.root.event_generate("<<RefreshVisibility>>")
        for listener in self.reset_tree_callback:
            listener()

    def notify_about_visibility_switch(self):
        print("Switching from "+str(self.visible)+" to "+str(not self.visible))
        self.visible = not self.visible

        if self.visible:
            self.ui_hider.notify_about_action()
            self.__build_ui()
        else:
            self.ui_hider.notify_about_explicit_hide()
            self.__hide_ui()

    def notify_about_current_state_change(self, node, emit=True):
        self.current_node = node
        if emit:
            self.ui_hider.notify_about_action()
            self.__build_ui()

    def __hide_ui(self):
        for child in self.root.winfo_children():
            child.destroy()

    def __build_ui(self):
        for child in self.root.winfo_children():
            child.destroy()

        frame = tk.Frame(self.root, background="white")
        frame.grid(sticky=tk.W)
        if self.current_node is None:
            return
        children = self.current_node.children

        for index, child in enumerate(children):
            label = tk.Label(frame, text="["+str(index+1)+"] " + child.label)
            color = "green"
            if child.is_message:
                color = "orange"
            label.config(foreground=color, background="white", font="fixedsys 10")
            label.grid(sticky=tk.W)
        up_label_text = "Go Up"
        if self.current_node.parent is None:
            up_label_text = "Hide"
        up_label = tk.Label(frame, text="[0] "+up_label_text)
        up_label.config(foreground="cyan", background="white", font="fixedsys 10")
        up_label.grid(sticky=tk.W)
