"""
description:
    Windowのテストを行います。
"""
from control.checker_window import CheckerWindow

try:
    window = CheckerWindow()
    window.create_window()
    window.show_window()
except Exception as e:  # pylint: disable=broad-except
    print("error")
    print(e)
