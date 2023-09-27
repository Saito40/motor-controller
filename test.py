import math, sys, os, time
import RPi.GPIO as GPIO

def istrue(check_num):
    if 20 < math.pow(check_num):
        return True
    else: return False

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

for i in range(10):
    print(i)
    if istrue(i):
        GPIO.output(17, GPIO.LOW)
    else:
        GPIO.output(17, GPIO.HIGH)


GPIO.cleanup()

