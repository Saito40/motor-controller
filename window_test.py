"""
description:
    Windowのテストを行います。
"""
import dataclasses
from control.window import Window
from control.time_data import TimerData, RapData
import setting


@dataclasses.dataclass
class mc:  # pylint: disable=C0103, C0115
    speed_step = len(setting.A_LED_PIN_LIST) - 1

    volume_separate = []
    _max_per_all = setting.VOLUME_MAX / setting.VOLUME_ROTATE_DEG
    _sign_transformation = 1
    if setting.VOLUME_SPEED_MAX_DEG < setting.VOLUME_SPEED_MIN_DEG:
        _sign_transformation = -1
    _volume_min = setting.VOLUME_SPEED_MIN_DEG \
        * _max_per_all \
        * _sign_transformation
    _volume_max = setting.VOLUME_SPEED_MAX_DEG \
        * _max_per_all \
        * _sign_transformation
    _volume_d_4 = (_volume_max - _volume_min)/4
    for i in range(1, speed_step+1):
        volume_separate.append(i * _volume_d_4 + _volume_min)
    print("volume_separate")
    print(volume_separate)

    volume_range_min = setting.VOLUME_RANGE_MIN_DEG * _max_per_all
    volume_range_max = setting.VOLUME_RANGE_MAX_DEG * _max_per_all
    print(volume_range_min, volume_range_max)

    def __init__(self):
        self.rap_data = RapData()
        self.rap_data.volume = 0
        self.volume_func = mc.check_volume(self)
        self.move = False

    @staticmethod
    def check_volume(motor_control):
        """
        description:
            ボリュームをチェックします。
        """
        def inner():
            volume = motor_control.rap_data.volume
            motor_speed_id = 0
            if mc.volume_range_min < volume < mc.volume_range_max:
                volume *= mc._sign_transformation
                for vs in mc.volume_separate:
                    if vs < volume:
                        motor_speed_id += 1

            Window.speed_change(motor_control.rap_data, motor_speed_id)

        return inner


mcs = [
    mc(),
    mc(),
]
window = Window(mcs, TimerData())
window.create_window(debug=True)
window.show_window()
