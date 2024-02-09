"""
description:
    このファイルは、水平方向にスケールを表示するためのクラスのファイルです。
"""

import tkinter


class HScale(tkinter.Scale):
    """
    description:
        horizontal scale
        水平方向にスケールを表示します。
    """
    def __init__(self, *args, **kwargs):
        kwargs["orient"] = tkinter.HORIZONTAL
        super().__init__(*args, **kwargs)
