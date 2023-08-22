#!/usr/bin/env python
# -*- coding: utf-8 -*-

## 設定
# ピン番号
A_ROTARY_CLK_A_PIN   = 1
A_ROTARY_DT__B_PIN   = 2
A_LED_R__PIN         = 3
A_LED_Y1_PIN         = 4
A_LED_Y2_PIN         = 5
A_LED_Y3_PIN         = 6
A_MOTOR_FW_PIN       = 7
A_SW_START_PIN       = 8
A_SW_GOAL_PIN        = 9

B_ROTARY_CLK_A_PIN   = 10
B_ROTARY_DT__B_PIN   = 11
B_LED_R_PIN          = 12
B_LED_Y1_PIN         = 13
B_LED_Y2_PIN         = 14
B_LED_Y3_PIN         = 15
B_MOTOR_FW_PIN       = 16
B_SW_START_PIN       = 17
B_SW_GOAL_PIN        = 18

# モーターの速度
# 0 < MOTOR_SPEED < 15(motor=3V) < 100(MAX)
MOTOR_LOW_SPEED  = 10
MOTOR_HIGH_SPEED = 15
MOTOR_SPEED_STEP = 3

import MotorControl.MotorControl as MotorControl
import MotorControl.SpeedChange as SpeedChange

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
    
def ckeck():
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
    ckeck()
    main()
