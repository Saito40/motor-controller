from threading import Event
from gpiozero import RotaryEncoder, Button
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO

STOP_SPEED = 0.
PWM_FREQ = 100 #Hz
ROTARY_MAX_STEPS = 200

class SpeedChange:
    speed_list = [STOP_SPEED]

    def __init__(self, name = "changer"):
        self.factory = PiGPIOFactory()
        self.name = name

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
            max_steps=ROTARY_MAX_STEPS, pin_factory=self.factory
        )
        self.rotor.steps = 0

        self.start_btn = Button(self.pin_sw_start, pull_up=True, pin_factory=self.factory)
        self.goal_btn  = Button(self.pin_sw_goal , pull_up=True, pin_factory=self.factory)
    
    def run(self):
        def change_rotor():
            print(f"{self.name}: rotor.steps is {self.rotor.steps}")
            motor_speed_id = self.rotor.steps
            if motor_speed_id < 0:
                motor_speed_id = 0
            if len(self.speed_list)-1 < motor_speed_id:
                motor_speed_id = len(self.speed_list)-1
            self.motor_fw_pwm.ChangeDutyCycle(self.speed_list[motor_speed_id])
            for i in range(len(self.led_pin_list)):
                GPIO.output(self.led_pin_list[i], i == motor_speed_id)

        def stop_script():
            print(f"{self.name}:Exiting")
            self.done.set()
            self.done = Event()
    
        # ロータリーエンコーダ変化時の処理
        self.rotor.when_rotated = change_rotor
        
        # ボタンリリース時の処理
        self.goal_btn.when_released = stop_script

        self.done.wait()

    @staticmethod
    def set_motor_speed(hi_speed: float, low_speed: float, speed_step: int):
        SpeedChange.speed_list = [STOP_SPEED]
        for i in range(speed_step):
            SpeedChange.speed_list.append(
                (hi_speed - low_speed) * i / (speed_step-1) 
                + low_speed)