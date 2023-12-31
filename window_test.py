"""
description:
    Windowのテストを行います。
"""
import dataclasses
from control.window import Window
from control.time_data import TimerData, RapData


@dataclasses.dataclass
class mc:  # pylint: disable=C0103, C0115
    def __init__(self):
        self.rap_data = RapData()
        self.volume_func = lambda: None
        self.move = False


mcs = [
    mc(),
    mc(),
]
window = Window(mcs, TimerData())
window.create_window(debug=True)
window.show_window()
