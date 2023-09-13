from threading import Event
from gpiozero import RotaryEncoder, Button
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from MotorControl.SpeedChange import SpeedChange
from MotorControl.TimeData import TimeData
from MotorControl.Factory import FACTORY
from datetime import datetime, timedelta
from MainWindow import INTERVAL, MainWindow

GPIO.setmode(GPIO.BCM)

class MotorControl:
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
        self.start_btn = Button(self.pin_sw_start, pull_up=True, pin_factory=FACTORY)
        self.goal_btn  = Button(self.pin_sw_goal , pull_up=True, pin_factory=FACTORY)

    def run(self):
        # ボタンリリース時の処理
        func = MotorControl.start_script(self)
        self.start_btn.when_released = func

        # ボタンリリース時の処理
        func = MotorControl.stop_script(self)
        self.goal_btn.when_released = func

        self.speed_change.run()

    @staticmethod
    def start_script(motor_control):
        def inner():
            print(f"{motor_control.speed_change.name}:start")
            
            # MainWindow.update_time(timedata)
            # 計測中でなければ時間計測開始
            if not motor_control.speed_change.timedata.start_flag:
                
                # 計測中フラグをON
                motor_control.speed_change.timedata.start_flag = True

                # 計測開始時刻を取得
                # start_time = time.time()
                motor_control.speed_change.timedata.start_time = datetime.now()

                # update_timeをINTERVAL[ms] 後に実行
                motor_control.speed_change.timedata.after_id = MainWindow.Root.after(
                    INTERVAL, lambda:MainWindow.update_time(motor_control.speed_change.timedata))
        return inner

    @staticmethod
    def stop_script(motor_control):
        def inner():
            print(f"{motor_control.speed_change.name}:Exiting")
            motor_control.speed_change.timedata.start_flag = False
            # motor_control.speed_change.done.set()
            # motor_control.speed_change.done = Event()
        return inner

