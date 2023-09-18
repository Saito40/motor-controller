# from threading import Event
from gpiozero import RotaryEncoder, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from MainWindow import MainWindow
from MotorControl.TimeData import TimeData
from MotorControl.Factory import FACTORY
import RPi.GPIO as GPIO
# import pigpio
# pi = pigpio.pi()
from setting import *

class SpeedChange:
    speed_list = [STOP_SPEED]

    def __init__(self, name = "changer"):
        self.name = name
        self.move = False
        self.timedata = TimeData()

    def set_pins(self, 
                 pin_rotary_a: int, 
                 pin_rotary_b: int, 
                 pin_motor_fw: int,
                 pin_led_r : int ,
                 pin_led_y1: int,
                 pin_led_y2: int,
                 pin_led_y3: int):
        self.pin_rotary_a = pin_rotary_a
        self.pin_rotary_b = pin_rotary_b
        self.pin_motor_fw = pin_motor_fw
        self.pin_led_r    = pin_led_r
        self.pin_led_y1   = pin_led_y1
        self.pin_led_y2   = pin_led_y2
        self.pin_led_y3   = pin_led_y3
        self.reset()

    def reset(self):
        GPIO.setup(self.pin_motor_fw, GPIO.OUT)
        self.motor_fw_pwm = GPIO.PWM(self.pin_motor_fw, PWM_FREQ)
        self.motor_fw_pwm.start(STOP_SPEED)
        
        self.led_pin_list = [self.pin_led_r, self.pin_led_y1, self.pin_led_y2, self.pin_led_y3]
        for pin in self.led_pin_list:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.output(self.led_pin_list[0], True)

        # ロータリーエンコーダ/ボタンのピン設定
        self.rotor = RotaryEncoder(
            self.pin_rotary_a, self.pin_rotary_b, wrap=True, 
            max_steps=ROTARY_MAX_STEPS, pin_factory=FACTORY
        )
        self.rotor.steps = 0

        # ロータリーエンコーダ変化時の処理
        func = SpeedChange.change_rotor(self)
        self.rotor.when_rotated = func
        
        # self.done.wait()

    @staticmethod
    def set_motor_speed(hi_speed: float, low_speed: float, speed_step: int):
        SpeedChange.speed_list = [STOP_SPEED]
        for i in range(speed_step):
            SpeedChange.speed_list.append(
                (hi_speed - low_speed) * i / (speed_step-1) 
                + low_speed)

    @staticmethod
    def change_rotor(speed_change):
        def inner():
            print(f"{speed_change.name}: rotor.steps is {speed_change.rotor.steps}")
            motor_speed_id = speed_change.rotor.steps
            if motor_speed_id < 0:
                motor_speed_id = 0
            if len(speed_change.speed_list)-1 < motor_speed_id:
                motor_speed_id = len(speed_change.speed_list)-1
            for i, pin in enumerate(speed_change.led_pin_list):
                GPIO.output(pin, i == motor_speed_id)
            MainWindow.speed_change(speed_change.timedata, motor_speed_id)

            if not speed_change.timedata.move: return
            # duty = speed_change.speed_list[motor_speed_id]
            # duty = int((duty * 1000000 / 100))
            # pi.hardware_PWM(speed_change.pin_motor_fw, PWM_FREQ, duty)
            speed_change.motor_fw_pwm.ChangeDutyCycle(speed_change.speed_list[motor_speed_id])
        return inner
