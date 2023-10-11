"""
description:
    モーターの制御を行います。
"""
from __future__ import annotations
import copy
from RPi import GPIO  # pylint: disable=E0401
from gpiozero import Button  # pylint: disable=E0401
from gpiozero.pins.pigpio import PiGPIOFactory  # pylint: disable=E0401
import spidev  # pylint: disable=E0401
from control.time_data import RapData, TimerData
from control.window import Window
import setting
# import pigpio
# pi = pigpio.pi()

GPIO.setmode(GPIO.BCM)


class MotorControl:
    """
    description:
        モーターの制御を行います。
    """
    FACTORY = PiGPIOFactory()
    speed_list = [setting.STOP_SPEED]
    # SPI通信を行うための準備
    spi = spidev.SpiDev()                    # インスタンスを生成
    spi.open(0, 0)                           # CE0(24番ピン)を指定
    spi.max_speed_hz = setting.MAX_SPEED_HZ  # 転送速度 1MHz

    speed_step = len(setting.A_LED_PIN_LIST) - 1

    volume_separate = []
    _max_per_all = setting.VOLUME_MAX / setting.VOLUME_ROTATE_DEG
    _volume_min = setting.VOLUME_SPEED_MIN_DEG * _max_per_all
    _volume_max = setting.VOLUME_SPEED_MAX_DEG * _max_per_all
    _volume_d_4 = (_volume_min - _volume_max)/4
    for i in range(1, speed_step+1):
        volume_separate.append(-i * _volume_d_4 + _volume_min)
    print(volume_separate)

    volume_range_min = setting.VOLUME_RANGE_MIN_DEG * _max_per_all
    volume_range_max = setting.VOLUME_RANGE_MAX_DEG * _max_per_all

    xfer2_l_in_l = [[0x68, 0x00], [0x78, 0x00]]
    id_counter = 0

    speed_list = [setting.STOP_SPEED]
    for i in range(speed_step):
        speed_list.append(
            (setting.MOTOR_HIGH_SPEED - setting.MOTOR_LOW__SPEED) * i
            / (speed_step-1)
            + setting.MOTOR_LOW__SPEED
            )

    def __init__(self, timer_data: TimerData, name="control"):
        self.timer_data = timer_data
        self.name = name
        self.pin_led_list = []
        self.pin_sw_rap = -1
        self.pin_motor_fw = -1
        self.rap_button = None
        self.move = False
        self.rap_data = RapData()
        self.spi_xfer2_list = \
            MotorControl.xfer2_l_in_l[MotorControl.id_counter]
        MotorControl.id_counter += 1
        self.motor_fw_pwm = None
        self.volume_func = None

    def set_pins(self,
                 pin_led_list: list[int],
                 pin_motor_fw: int,
                 pin_sw_rap: int = None):
        """
        description:
            ピンを設定します。
        """
        self.pin_led_list = pin_led_list
        self.pin_sw_rap = pin_sw_rap
        self.pin_motor_fw = pin_motor_fw
        self.reset()

    def reset(self):
        """
        description:
            リセットします。
        """
        self.rap_button = Button(
            self.pin_sw_rap,
            pull_up=True,
            pin_factory=MotorControl.FACTORY,
            bounce_time=1e-7
            )
        # ボタンリリース時の処理
        func = MotorControl.rap_script(self, self.timer_data)
        self.rap_button.when_released = func

        GPIO.setup(self.pin_motor_fw, GPIO.OUT)
        self.motor_fw_pwm = GPIO.PWM(self.pin_motor_fw, setting.PWM_FREQ)
        self.motor_fw_pwm.start(setting.STOP_SPEED)

        for pin in self.pin_led_list:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.output(self.pin_led_list[0], True)

        self.volume_func = MotorControl.check_volume(self)

    @staticmethod
    def rap_script(motor_control: MotorControl, timer_data: TimerData):
        """
        description:
            ラップとストップを行います。
        """
        def inner():
            timer_data.rap_and_stop(motor_control.rap_data)
        return inner

    @staticmethod
    def changed_rotor(motor_control: MotorControl):
        """
        description:
            ローターが変更されたときに呼び出されます。
        """
        def inner():
            name = motor_control.name
            steps = motor_control.rotor.steps
            print(f"{name}: rotor.steps is {steps}")
            motor_speed_id = steps
            motor_speed_id = max(motor_speed_id, 0)
            motor_speed_id = min(
                motor_speed_id,
                len(motor_control.speed_list)-1
            )
            for i, pin in enumerate(motor_control.pin_led_list):
                GPIO.output(pin, i == motor_speed_id)
            Window.speed_change(motor_control.rap_data, motor_speed_id)

            if not motor_control.rap_data.move:
                return
            # duty = motor_control.speed_list[motor_speed_id]
            # duty = int((duty * 1000000 / 100))
            # pi.hardware_PWM(
            #   motor_control.pin_motor_fw, setting.PWM_FREQ,
            #   duty)
            motor_control.motor_fw_pwm.ChangeDutyCycle(
                motor_control.speed_list[motor_speed_id])
        return inner

    @staticmethod
    def check_volume(motor_control: MotorControl):
        """
        description:
            ボリュームをチェックします。
        """
        def inner():
            # SPI通信で値を読み込む
            resp = MotorControl.spi.xfer2(
                copy.deepcopy(motor_control.spi_xfer2_list))
            volume = ((resp[0] << 8) + resp[1]) & 0x3FF  # 読み込んだ値を10ビットの数値に変換

            motor_speed_id = 0
            if MotorControl.volume_separate[0] < volume:
                motor_speed_id = 0
            else:
                for i in range(len(MotorControl.volume_separate)-1):
                    if volume < MotorControl.volume_separate[i] and \
                            MotorControl.volume_separate[i+1] <= volume:
                        motor_speed_id = i+1
                        break
                else:
                    motor_speed_id = MotorControl.speed_step
            if not MotorControl.volume_range_min < volume \
                    < MotorControl.volume_range_max:
                motor_speed_id = 0

            for i, pin in enumerate(motor_control.pin_led_list):
                GPIO.output(pin, i == motor_speed_id)
            Window.speed_change(motor_control.rap_data, motor_speed_id)

            if not motor_control.rap_data.move:
                return
            # duty = motor_control.speed_list[motor_speed_id]
            # duty = int((duty * 1000000 / 100))
            # pi.hardware_PWM(
            #   motor_control.pin_motor_fw,
            #   setting.PWM_FREQ,
            #   duty)
            motor_control.motor_fw_pwm.ChangeDutyCycle(
                motor_control.speed_list[motor_speed_id])
        return inner

    @staticmethod
    def close():
        """
        description:
            spiを閉じます。
        """
        MotorControl.spi.close()
