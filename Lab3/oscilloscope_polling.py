import time

import RPi.GPIO as GPIO # type: ignore

import board # type: ignore
import busio # type: ignore
import math

import adafruit_mcp4725 # type: ignore


# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725.
dac = adafruit_mcp4725.MCP4725(i2c)

outPin = 4

button = 26

GPIO.setmode(GPIO.BCM)

GPIO.setup(outPin, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def stop_wave():
    dac.raw_value = int(0)
    GPIO.output(outPin, GPIO.LOW)

def button_logic():
    if GPIO.input(button) == GPIO.LOW:
        stop_wave()
        waveform_type = str(input("Choose a waveform type (sq/sin/tri): "))
        while True:
            if (waveform_type == "sq" or waveform_type == "sin" or waveform_type == "tri"):
                inputVmax = float(input("What is your desired maximum voltage? (Vmax): "))
                inputFreq = float(input("What is your desired frequency? (freq): "))
                if (waveform_type == "sq"):
                    print("Outputting Square Wave")
                    print("Press the button again to start a new waveform")
                    square_wave(inputVmax, inputFreq)
                elif waveform_type == "sin":
                    print("Outputting Sine Wave")
                    print("Press the button again to start a new waveform")
                    sin_wave(inputVmax, inputFreq)
                elif waveform_type == "tri":
                    print("Outputting Triangle Wave")
                    print("Press the button again to start a new waveform")
                    triangle_wave(inputVmax, inputFreq)
                else:
                    print("Invalid input, please try again.")
            else:
                # print(waveform_type, type(waveform_type))
                print("Invalid input, please try again.")
    else:
        pass

def square_wave(Vmax, freq):
    # Uses the DAC to convert the function inputs to obtain a waveform via the AD2

    # function inputs: 
    # freq is the desired frequency in Hz
    # Vmax is the maximum desired output voltage in Volts

    t = 0.0 # starting time

    # tStep = 0.05 # time steps # no longer in use

    while True:
        start = time.time()
        # tStep is based on execution time

        if ((t%float(1/freq)) > (float(1/freq)/2)):
            # "1/freq" is the period
            # if the amount of time modulo the period is greater than half the period

            dac.raw_value = int((4095 * Vmax)/3.3)
                # 4095 is the raw 12-bit output of the DAC
                # dac.raw_value is for the Vmax in bits (not Volts)
                # 3.3 Volts is the input voltage from our raspberry pi
                # this is converting the inputted Vmax into bits, and setting it in the DAC
        else:
            dac.raw_value = 0


        
        t += time.time() - start
        # this is the new tStep

        button_logic()

def sin_wave(Vmax, freq):
    t = 0.0

    tStep = 0.05

    Vmax_raw_value = (Vmax*4095)/3.3

    while True:
        start = time.time()
        
        #THIS VARIABLE voltage IS IN BITS:
        voltage = (Vmax_raw_value/2) +  (Vmax_raw_value) * (0.5* math.sin((6.2832*freq)*t)) # increasing what's inside of sin, increases the frequency
        
        dac.raw_value = int((voltage))

        t+=time.time()-start
        # t+=tStep
        # time.sleep(0.0005)

        button_logic()

def triangle_wave(Vmax, freq):
    # Input Vmax in Volts and freq in Hz

    t = 0.0
    # tStep = 0.05 # no longer in use

    Vmax_raw_value = int((4095*Vmax)/3.3)

    while True:
        start = time.time()
        if (t == 0):
            dac.raw_value = 0
        elif ((t%float(1/freq)) < (float(1/freq)*0.5)):
            dac.raw_value = int((Vmax_raw_value*2*(freq))*(t%(1/freq)))
            # equation for the line: 2Vmax*T * (t % T); T=period=(1/freq)
        else:
            dac.raw_value = int(((-1)*Vmax_raw_value*2*(freq))*(t%(1/freq))+(2*Vmax_raw_value))
            # equation for the line: -2Vmax*T * (t % T) + 2Vmax; T=period=(1/freq); adding 2Vmax for y-int for negative slope
        
        t += time.time() - start
        # this is the new tStep

        button_logic()


def main():
    # print("Howdy! Welcome to Segun's and Katelyn's Lab 2 Oscilloscope!")
    # print("Press the button to begin.")
    try:
        while True:
            time.sleep(0.1)
            button_logic()

    finally:
        stop_wave()
        GPIO.cleanup()

if __name__ == "__main__":
    main()