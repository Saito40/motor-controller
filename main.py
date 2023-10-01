#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python -V 3.9.2

## 設定
# ピン番号
A_ROTARY_A_PIN   =  1
A_ROTARY_B_PIN   =  2
A_ROTARY_BTN_PIN =  3
A_LED_R__PIN     =  4
A_LED_Y1_PIN     =  5
A_LED_Y2_PIN     =  6
A_LED_Y3_PIN     =  7
A_MOTOR_FW_PIN   =  8
A_SW_START_PIN   =  9
A_SW_GOAL_PIN    = 10

# B_ROTARY_A_PIN   = 11
# B_ROTARY_B_PIN   = 12
# B_ROTARY_BTN_PIN = 13
# B_LED_R_PIN      = 14
# B_LED_Y1_PIN     = 15
# B_LED_Y2_PIN     = 16
# B_LED_Y3_PIN     = 17
# B_MOTOR_FW_PIN   = 18
# B_SW_START_PIN   = 19
# B_SW_GOAL_PIN    = 10

# モーターの速度
# 0 < MOTOR_SPEED < 15 < 100(MAX)
MOTOR_LOW_SPEED  = 10
MOTOR_HIGH_SPEED = 15

from threading import Event
from gpiozero import RotaryEncoder, Button
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO

motor_speed_list = [0]
motor_speed_range = 2
for i in range(motor_speed_range+1):
    motor_speed_list.append(
        (MOTOR_HIGH_SPEED - MOTOR_LOW_SPEED) * i / motor_speed_range 
        + MOTOR_LOW_SPEED)
# print(motor_speed_list)

# motor_speed_dict = {}
# motor_speed_dict["STOP"]   = {"value" : motor_speed_list[0], "pin" : A_LED_R__PIN}
# motor_speed_dict["SPEED1"] = {"value" : motor_speed_list[1], "pin" : A_LED_Y1_PIN}
# motor_speed_dict["SPEED2"] = {"value" : motor_speed_list[2], "pin" : A_LED_Y2_PIN}
# motor_speed_dict["SPEED3"] = {"value" : motor_speed_list[3], "pin" : A_LED_Y3_PIN}
# print(motor_speed_dict)

def main():
    print("Hello World!")
    GPIO.setmode(GPIO.BCM)

    ############################
    ## モーターの設定          ##
    ############################
    GPIO.setup(A_MOTOR_FW_PIN, GPIO.OUT)
    motor_fw = GPIO.PWM(A_MOTOR_FW_PIN, 100) #100Hz
    motor_fw.start(0)

    ############################
    ## LEDの設定               ##
    ############################
    led_pin_list = [A_LED_R__PIN, A_LED_Y1_PIN, A_LED_Y2_PIN, A_LED_Y3_PIN]
    for pin in led_pin_list:
        GPIO.setup(pin, GPIO.OUT)
    GPIO.output(led_pin_list[0], 1)
    
    ############################
    ## ロータリースイッチの設定 ##
    ############################
    factory = PiGPIOFactory()

    # ロータリーエンコーダ/ボタンのピン設定
    rotor = RotaryEncoder(
        A_ROTARY_A_PIN, A_ROTARY_B_PIN, wrap=True, max_steps=20, pin_factory=factory
    )
    rotor.steps = 0
    btn = Button(A_ROTARY_BTN_PIN, pull_up=True, pin_factory=factory)
    done = Event()

    def change_rotor():
        # rotor steps (-180..180) to 0..1
        print(f"rotor.steps is {rotor.steps}")
        motor_speed_id = rotor.steps
        if motor_speed_id < 0:
            motor_speed_id = 0
        if len(motor_speed_list)-1 < motor_speed_id:
            motor_speed_id = len(motor_speed_list)-1
        motor_fw.ChangeDutyCycle(motor_speed_list[motor_speed_id])

    def stop_script():
        print("Exiting")
        done.set()

    # ロータリーエンコーダ変化時の処理
    rotor.when_rotated = change_rotor

    # ボタンリリース時の処理
    btn.when_released = stop_script

    done.wait()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
