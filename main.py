# coding=utf-8
import json

from data_node import DataNode, parse_json, DataNodeState
import keyboard_input
from ui import UIOverlay

datastate: DataNodeState
dataRootNode: DataNode

with open("messages.json", "r") as msgJson:
    data = json.load(msgJson)
    dataRootNode = parse_json(data)
    pass


keyboard_input.init()
ui = UIOverlay()

datastate = DataNodeState(dataRootNode, ui)
ui.notify_about_current_state_change(dataRootNode)
keyboard_input.add_listener(datastate.notify_about_keypress)
ui.root.mainloop()
