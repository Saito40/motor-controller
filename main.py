#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setting import *

from MotorControl.MotorControl import MotorControl
from MotorControl.SpeedChange import SpeedChange
from MainWindow import MainWindow
import RPi.GPIO as GPIO

def main():
    controlA = MotorControl("controlA")
    controlB = MotorControl("controlB")

    SpeedChange.set_motor_speed(MOTOR_HIGH_SPEED, MOTOR_LOW_SPEED, MOTOR_SPEED_STEP)

    controlA.set_pins(
        A_ROTARY_CLK_A_PIN, 
        A_ROTARY_DT__B_PIN, 
        A_LED_R__PIN      , 
        A_LED_Y1_PIN      , 
        A_LED_Y2_PIN      , 
        A_LED_Y3_PIN      , 
        A_MOTOR_FW_PIN    , 
        A_SW_START_PIN    , 
        A_SW_GOAL_PIN     )

    controlB.set_pins(
        B_ROTARY_CLK_A_PIN, 
        B_ROTARY_DT__B_PIN, 
        B_LED_R_PIN       , 
        B_LED_Y1_PIN      , 
        B_LED_Y2_PIN      , 
        B_LED_Y3_PIN      , 
        B_MOTOR_FW_PIN    , 
        B_SW_START_PIN    , 
        B_SW_GOAL_PIN     )
    
    # ディスプレイ表示

    # モーター制御
    controlA.speed_change.move = True
    controlB.speed_change.move = True
    controlA.run()
    controlB.run()
    main = MainWindow([controlA, controlB])
    
def check():
    pins = [
        A_ROTARY_CLK_A_PIN ,
        A_ROTARY_DT__B_PIN ,
        A_LED_R__PIN       ,
        A_LED_Y1_PIN       ,
        A_LED_Y2_PIN       ,
        A_LED_Y3_PIN       ,
        A_MOTOR_FW_PIN     ,
        A_SW_START_PIN     ,
        A_SW_GOAL_PIN      ,
        B_ROTARY_CLK_A_PIN ,
        B_ROTARY_DT__B_PIN ,
        B_LED_R_PIN        ,
        B_LED_Y1_PIN       ,
        B_LED_Y2_PIN       ,
        B_LED_Y3_PIN       ,
        B_MOTOR_FW_PIN     ,
        B_SW_START_PIN     ,
        B_SW_GOAL_PIN      ]
    
    # ピン番号の重複チェック
    for i in range(len(pins)):
        for j in range(i+1, len(pins)):
            if pins[i] == pins[j]:
                print(f"pin number is duplicated {i} {j} {pins[i]}")
                exit(1)

    # モーターの速度チェック
    if MOTOR_LOW_SPEED > MOTOR_HIGH_SPEED:
        print(f"MOTOR_LOW_SPEED > MOTOR_HIGH_SPEED")
        exit(1)
    
    if MOTOR_HIGH_SPEED < 15:
        print("MOTOR_HIGH_SPEED < 15")
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
    except Exception as e:
        print(e)
        import sys
        tb = sys.exc_info()[2]
        print(e.with_traceback(tb))
        GPIO.cleanup()
