from typing import Optional
from ui import UIOverlay
from typing import Callable


class DataNode:
    def __init__(self, parent: Optional, message: Optional[str], opt_message_short: Optional[str]):
        self.message = message
        self.is_message = message is not None
        if opt_message_short is None:
            self.label = self.message[0:15]
            if len(self.label) == 15:
                self.label = self.message[0:12]+"..."
        else:
            self.label = opt_message_short[0:15]
        self.parent: Optional[DataNode] = parent
        if self.parent is not None:
            self.parent._add_child(self)
        self.children: list[DataNode] = []
        pass

    def _add_child(self, child):
        self.children.append(child)

    def __str__(self):
        prefix = "GROUP"
        if self.is_message:
            prefix = "TEXT"
        return prefix+"."+self.label


def __parse_as_node(parent: DataNode, data: dict) -> None:
    node = DataNode(parent, None, data["label"])
    list_of_children = data["node"]
    if not isinstance(list_of_children, list):
        raise Exception("Wrong Structure")
    for entry in list_of_children:
        __parse_entry(node, entry)


def __parse_as_message(parent: DataNode, data: dict) -> None:
    DataNode(parent, data["message"], data["label"])


def __parse_entry(parent: DataNode, data: dict) -> None:
    has_message = "message" in data.keys()
    has_node = "node" in data.keys()
    has_label = "label" in data.keys()
    if has_node and has_message:
        raise Exception("A node can only have either a Node or a Message")
    if has_node and not has_label:
        raise Exception("A node requires a label")

    if has_node:
        __parse_as_node(parent, data)
    elif has_message:
        __parse_as_message(parent, data)
    else:
        raise Exception("Invalid Node. Neither 'node' or 'message' found")


def parse_json(root_node: dict):
    root = DataNode(None, "", None)
    list_of_root_children = root_node["node"]
    if not isinstance(list_of_root_children, list):
        raise Exception("Wrong Structure")
    for entry in list_of_root_children:
        __parse_entry(root, entry)
    return root


class DataNodeState:
    def __init__(self, root: DataNode, ui: UIOverlay):
        self.current = root
        self.ui = ui
        self.ui.reset_tree_callback.append(self._set_root_without_emit)
        self.new_message_listeners: list[Callable[[str], None]] = []

    def _set_root_without_emit(self):
        while self.current.parent is not None:
            self.current = self.current.parent
        self.ui.notify_about_current_state_change(self.current, False)

    def notify_about_keypress(self, numpad_number: int):
        index = numpad_number - 1
        if index < 0:
            #  Try to go up
            if self.current.parent is None:
                print("Got command to go up, but is at root. ignoring")
                self.ui.notify_about_visibility_switch()
            else:
                self.current = self.current.parent
                self.ui.notify_about_current_state_change(self.current)
        elif index < len(self.current.children):
            # Change to child / or start writing message
            child = self.current.children[index]
            if child.is_message:
                print("Message is: "+child.message)
                self._notify_listeners_about_new_message(child.message)
            else:
                print("Changing to Child "+child.label)
                self.current = child
                self.ui.notify_about_current_state_change(self.current)
        else:
            print("Selected index out of bounds. Ignoring")

    def _notify_listeners_about_new_message(self, msg: str):
        for listener in self.new_message_listeners:
            listener(msg)
