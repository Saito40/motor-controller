"""
description:
    Windowのテストを行います。
"""
from RPi import GPIO  # pylint: disable=E0401
from control.checker_window import CheckerWindow, DummyControl
import setting

try:
    control_a = DummyControl()
    control_b = DummyControl()

    control_a.set_pins(
        setting.A_LED_PIN_LIST,
        setting.A_MOTOR_FW_PIN,
        setting.A_SW_RAP___PIN)

    control_b.set_pins(
        setting.B_LED_PIN_LIST,
        setting.B_MOTOR_FW_PIN,
        setting.B_SW_RAP___PIN)

    window = CheckerWindow(
        [control_a, control_b]
    )
    window.create_window()
    window.show_window()
except Exception as e:  # pylint: disable=broad-except
    print("error")
    print(e)

try:
    control_a.close()
    control_b.close()
finally:
    pass

try:
    GPIO.cleanup()
finally:
    pass

try:
    DummyControl.spi.close()
finally:
    pass
