"""
description:
    このファイルは、メインとなるファイルです。
    これを実行することで、プログラムが動きます。
"""
from RPi import GPIO  # pylint: disable=E0401
import setting
# from control.motor_control import MotorControl
# from control.label_data import TimerLabel
# from control.window import Window


def main():
    """
    description:
        この関数は、メイン関数です。
        この関数を実行することで、プログラムが動きます。
    """
    pass


def check():
    """
    description:
        この関数は、設定ファイルのチェックを行います。
        この関数を実行することで、設定ファイルのチェックが行われます。
    """
    pins = [
        setting.A_MOTOR_FW_PIN,
        setting.A_SW_RAP___PIN,
        setting.B_MOTOR_FW_PIN,
        setting.B_SW_RAP___PIN]
    pins.extend(setting.A_LED_PIN_LIST)
    pins.extend(setting.B_LED_PIN_LIST)
    pins.extend(setting.SPI_PIN)

    # ピン番号の重複チェック
    for i in range(len(pins)):  # pylint: disable=C0200
        for j in range(i+1, len(pins)):
            if pins[i] == pins[j]:
                raise RuntimeError(
                    f"pin number is duplicated {i} {j} {pins[i]}")

    # モーターの速度チェック
    if setting.MOTOR_LOW__SPEED > setting.MOTOR_HIGH_SPEED:
        raise RuntimeError("MOTOR_LOW_SPEED > MOTOR_HIGH_SPEED")

    if 15 < setting.MOTOR_HIGH_SPEED:
        print("15 < setting.MOTOR_HIGH_SPEED")
        while True:
            print("over 3V? [Y/n]")
            ans = input()
            if ans == "n":
                exit(1)
            elif ans == "Y":
                break


if __name__ == "__main__":
    check()
    try:
        main()
    except Exception as ex:  # pylint: disable=W0718
        print(ex)
    GPIO.cleanup()
