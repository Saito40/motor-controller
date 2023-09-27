"""
description: test
"""

import math
import RPi.GPIO as GPIO  # pylint: disable=E0401


def istrue(check_num):
    """
    description: return true if check_num is greater than 20
    """
    if 20 < math.pow(check_num):
        return True
    return False


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

for i in range(10):
    print(i)
    if istrue(i):
        GPIO.output(17, GPIO.LOW)
    else:
        GPIO.output(17, GPIO.HIGH)

GPIO.cleanup()
