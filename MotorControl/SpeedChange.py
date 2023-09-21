# from threading import Event
from MainWindow import MainWindow
from MotorControl.TimeData import TimeData
from MotorControl.Factory import FACTORY
import RPi.GPIO as GPIO
# import pigpio
# pi = pigpio.pi()
from setting import *
import spidev
import copy

class SpeedChange:
    speed_list = [STOP_SPEED]
    #SPI通信を行うための準備
    spi = spidev.SpiDev()               #インスタンスを生成
    spi.open(0, 0)                      #CE0(24番ピン)を指定
    spi.max_speed_hz = MAX_SPEED_HZ          #転送速度 1MHz
    volume_separate = []
    _volume_min = VOLUME_SPEED_MIN_DEG / VOLUME_MAX_DEG * VOLUME_MAX
    _volume_max = VOLUME_SPEED_MAX_DEG / VOLUME_MAX_DEG * VOLUME_MAX
    _volume_d_4 = (_volume_min - _volume_max)/4
    for i in range(1, MOTOR_SPEED_STEP+1):
        volume_separate.append(-i * _volume_d_4 + _volume_min)

    print(volume_separate)

    xfer2_l_in_l = [[0x68, 0x00], [0x78, 0x00]]
    id_counter = 0
 
    def __init__(self, name = "changer"):
        self.name = name
        self.move = False
        self.timedata = TimeData()
        self.spi_xfer2_list = SpeedChange.xfer2_l_in_l[SpeedChange.id_counter]
        SpeedChange.id_counter += 1

    def set_pins(self, 
                 pin_rotary_a: int, 
                 pin_rotary_b: int, 
                 pin_motor_fw: int,
                 pin_led_r : int ,
                 pin_led_y1: int,
                 pin_led_y2: int,
                 pin_led_y3: int):
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

        self.volume_func = SpeedChange.check_volume(self)

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
    
    @staticmethod
    def check_volume(speed_change):
        def inner():

            resp = SpeedChange.spi.xfer2(copy.deepcopy(speed_change.spi_xfer2_list))               #SPI通信で値を読み込む
            volume = ((resp[0] << 8) + resp[1]) & 0x3FF  #読み込んだ値を10ビットの数値に変換
            
            motor_speed_id = 0
            if SpeedChange.volume_separate[0] < volume:
                motor_speed_id = 0
            else:
                for i in range(len(SpeedChange.volume_separate)-1):
                    if volume < SpeedChange.volume_separate[i] and SpeedChange.volume_separate[i+1] <= volume:
                        motor_speed_id = i+1
                        break
                else:
                    motor_speed_id = MOTOR_SPEED_STEP

            print(f"{speed_change.name}: motor_speed_id is {motor_speed_id}")
            
            for i, pin in enumerate(speed_change.led_pin_list):
                GPIO.output(pin, i == motor_speed_id)
            MainWindow.speed_change(speed_change.timedata, motor_speed_id)

            if not speed_change.timedata.move: return
            # duty = speed_change.speed_list[motor_speed_id]
            # duty = int((duty * 1000000 / 100))
            # pi.hardware_PWM(speed_change.pin_motor_fw, PWM_FREQ, duty)
            speed_change.motor_fw_pwm.ChangeDutyCycle(speed_change.speed_list[motor_speed_id])
        return inner

    @staticmethod
    def close():
        SpeedChange.spi.close()
