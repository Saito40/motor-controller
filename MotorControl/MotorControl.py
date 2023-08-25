from threading import Event
from gpiozero import RotaryEncoder, Button
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
import MotorControl.SpeedChange as SpeedChange
import MotorControl.TimeData as TimeData

GPIO.setmode(GPIO.BCM)

class MotorControl:
    Factory = PiGPIOFactory()

    def __init__(self, name = "control"):
        self.speed_change = SpeedChange(name)
        self.name = name
    
    def set_pins(self, 
                pin_rotary_a: int,
                pin_rotary_b: int,
                pin_led_r: int,
                pin_led_y1: int,
                pin_led_y2: int,
                pin_led_y3: int,
                pin_motor_fw: int,
                pin_sw_start: int = None,
                pin_sw_goal: int = None):
        self.speed_change.set_pins(
            pin_rotary_a, 
            pin_rotary_b, 
            pin_motor_fw, 
            pin_led_r, 
            pin_led_y1, 
            pin_led_y2, 
            pin_led_y3)
        self.pin_sw_start = pin_sw_start
        self.pin_sw_goal  = pin_sw_goal
        self.reset()
    
    def reset(self):
        self.start_btn = Button(self.pin_sw_start, pull_up=True, pin_factory=MotorControl.Factory)
        self.goal_btn  = Button(self.pin_sw_goal , pull_up=True, pin_factory=MotorControl.Factory)

    def run(self):
        # ボタンリリース時の処理
        func = SpeedChange.stop_script(self)
        self.goal_btn.when_released = func

        self.speed_change.run()
