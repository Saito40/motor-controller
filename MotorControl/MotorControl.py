from __future__ import annotations
from gpiozero import Button
import RPi.GPIO as GPIO
from MotorControl.SpeedChange import SpeedChange
from MotorControl.TimeData import TimeData, TimeMain
from MotorControl.Factory import FACTORY
from datetime import datetime, timedelta
from MainWindow import INTERVAL, MainWindow
from setting import *

GPIO.setmode(GPIO.BCM)

class MotorControl:
    def __init__(self, name = "control"):
        self.speed_change = SpeedChange(name)
        self.name = name
    
    def set_pins(self, 
                pin_led_r: int,
                pin_led_y1: int,
                pin_led_y2: int,
                pin_led_y3: int,
                pin_motor_fw: int,
                pin_sw_rap: int = None):
        self.speed_change.set_pins(
            pin_motor_fw, 
            pin_led_r, 
            pin_led_y1, 
            pin_led_y2, 
            pin_led_y3)
        self.pin_sw_rap  = pin_sw_rap
        self.reset()
    
    def reset(self):
        # self.start_btn = Button(self.pin_sw_start, pull_up=True, pin_factory=FACTORY)
        self.rap_btn = Button(self.pin_sw_rap , pull_up=True, pin_factory=FACTORY)

    def run(self, time_main: TimeMain):
        # ボタンリリース時の処理
        func = MotorControl.rap_script(self, time_main)
        self.rap_btn.when_released = func

    @staticmethod
    def start_script(motor_control: MotorControl):
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
    def rap_script(motor_control: MotorControl, timemain: TimeMain):
        def inner():
            if not timemain.start_flag: return
            
            timedata = motor_control.speed_change.timedata
            if not timedata.start_flag: return
            rap_count = len(timedata.rap_times)
            time = datetime.now() - timemain.start_time
            if rap_count!=0:
                time = time - sum(timedata.rap_times, timedelta(0))
            if time < timedelta(seconds=TIME_SPAN): return
            timedata.rap_times.append(time)
            timedata.rap_labels[rap_count].config(
                text=rap_time_label_format(rap_count+1, MainWindow.time_to_str(time)))

            if RAP_COUNT <= len(timedata.rap_times):
                timedata.start_flag = False
                timedata.sum_label.config(
                    text=sum_time_label_format(
                        MainWindow.time_to_str(
                            sum(timedata.rap_times, timedelta(0))
                        )
                    )
                )
                
            if all([(not timedata.start_flag) for timedata in timemain.time_data_list]):
                timemain.start_flag = False
        return inner

