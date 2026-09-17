# sudo pip3 install adafruit-circuitpython-mpu6050

"""
Instructions
 Start with circuit (including MCP6050) at hip level.
 Prior to running the code, ensure that it is still. This will prevent any poor readings from any movement.
 Run the program with 'python gyro.py'.
 Upon running the program, first wait for calibration to complete.
 You will be prompted to begin taking steps after that.
"""

import board
import busio
import adafruit_mpu6050
import RPi.GPIO as GPIO

#perf_counter is more precise than time() for dt calculation
from time import sleep, perf_counter
import math
import numpy as np
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)




try:

    # BEGIN THE "CALIBRATION PHASE"

    print("Calibrating...")

    #read one data point while staying still to act as our calibration values
    x_acc, y_acc, z_acc = mpu.acceleration

    #calculate the magnitude, save as the control/calibration value
    calib_mag = math.sqrt(x_acc**2+y_acc**2+z_acc**2) 

    print("\n*******************\nBegin Stepping...\n*******************")
    sleep(1)




    # BEGIN THE "MOVEMENT PHASE"

    step_count = 0
    start_time = perf_counter()

    #write a loop to poll each sensor and print its axis values
    while ((perf_counter() - start_time) < 60 and step_count < 52):
        #raed a new data point (x,y,z) of acceleration from the MCP6050
        x_acc, y_acc, z_acc = mpu.acceleration

        print("")
        sleep(0.1)

        #calculate the magnitude of the acceleration
        mag = math.sqrt(x_acc**2+y_acc**2+z_acc**2)

        #if the current magnitude is outside +-10% of the calibrated magnitude, count it as a step
        if (mag < 0.9*calib_mag or mag > 1.1*calib_mag):
            step_count += 1
            print("step count: ",step_count)

            #delay to avoid double counting a step
            sleep(.4)

finally:
    GPIO.cleanup()
