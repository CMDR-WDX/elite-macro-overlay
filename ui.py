import tkinter as tk


def _make_overlay(frame: tk.Tk):
    """
    Creates an overlay frame. This code has been taken from
    https://github.com/notatallshaw/fall_guys_ping_estimate/blob/296ce8207ce8b8f4240d29fbb422d7df0710bcfa/fgpe/overlay.py
    :param frame: The Frame to create an Overlay from
    """
    frame.overrideredirect(True)
    frame.config(background="white")
    frame.geometry("+10+10")
    frame.wm_attributes("-topmost", True)
    frame.wm_attributes("-transparentcolor", "white")



class UIOverlay:
    def __init__(self):
        self.root = tk.Tk()
        _make_overlay(self.root)


    def notify_about_current_state_change(self, node):
        for child in self.root.winfo_children():
            child.destroy()

        children = node.children
        frame = tk.Frame(self.root, background="white")
        frame.grid(sticky=tk.W)
        for index, child in enumerate(children):
            label = tk.Label(frame, text="["+str(index+1)+"] " + child.label)
            color = "green"
            if child.is_message:
                color = "orange"
            label.config(foreground=color, background="white", font="fixedsys 20")
            label.grid(sticky=tk.W)
        up_label_text = "Go Up"
        if node.parent is None:
            up_label_text = "Hide"
        up_label = tk.Label(frame, text="[0] "+up_label_text)
        up_label.config(foreground="cyan", background="white", font="fixedsys 20")
        up_label.grid(sticky=tk.W)


