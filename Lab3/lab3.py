import time
import RPi.GPIO as GPIO
import board
import busio
import digitalio
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

"""
NOTE TO OUR GRADER:

This code only provides accurate when the AD2 generates a wave where there is an offset (usually equal to) the input amplitude.

"""


# Initialize SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# chip select
cs = digitalio.DigitalInOut(board.D22)

# mcp3008 chip
mcp = MCP.MCP3008(spi, cs)

outPin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(outPin, GPIO.OUT, initial=GPIO.LOW)

channel1 = AnalogIn(mcp, MCP.P0)


def get_data():
    # reads a time and voltage value
    x_points.append(time.time())
    y_points.append(channel1.value)

def dynamic_threshold(data, factor=0.2):
    return np.mean(np.abs(data)) * factor

def moving_avg(y_data, sma_size):
    new_data = []
    for i in range(len(y_data)-sma_size):
        sum = np.sum(y_data[i:i+sma_size])
        avg = sum/sma_size
        new_data.append(avg)
    return new_data

def print_graph(x_points, y_points, filename = str(int(time.time()))+".png"):
    # fig = plt.figure()
    plt.plot(x_points, y_points)
    # test_shape = input("what wave shape are you testing? ")
    print("filename: ",filename,"\n")
    plt.savefig(filename)
    plt.clf()


def eliminate_square_shape(first_deriv):
    first_deriv_len = len(first_deriv)

    flat_threshold = dynamic_threshold(first_deriv, factor=0.1)
    slope_change_threshold = dynamic_threshold(first_deriv, factor=0.5)
    # second_derivative_threshold = dynamic_threshold(second_derivatives, factor=0.5)

    # Square Wave Check: Look for flat regions (near-zero slopes) and abrupt changes
    flat_regions = np.sum(np.abs(first_deriv) < flat_threshold)
    abrupt_changes = np.sum(np.abs(np.diff(first_deriv)) > slope_change_threshold)
    
    if flat_regions > first_deriv_len // 3 and abrupt_changes >= 2:
        return "Square Wave"
    
    return "Not Square Wave"


def get_freq(x_points, y_points_smoothed, wave_type):
    if wave_type == "Square Wave":
        # Square wave frequency detection by counting rising edges only
        threshold = (max(y_points_smoothed) + min(y_points_smoothed)) / 2
        # Detect rising edges (where the signal crosses the threshold upwards)
        crossings = np.where((y_points_smoothed[:-1] < threshold) & (y_points_smoothed[1:] >= threshold))[0]
        if len(crossings) < 2:
            print("Not enough crossings to determine frequency.")
            return None
        crossing_times = [x_points[c] for c in crossings]
        periods = np.diff(crossing_times)
        if len(periods) > 0:
            avg_period = np.mean(periods)
            frequency = 1 / avg_period
            print(f"Frequency = {frequency} Hz")
            return frequency
        else:
            print("Not enough data to calculate frequency.")
            return None
    else:
        # Use only high peaks (local maxima) for sine and triangle waves
        high_peaks, _ = find_peaks(y_points_smoothed)
        
        if len(high_peaks) < 2:
            print("Not enough peaks to determine frequency.")
            return None
        
        peak_times = np.array([x_points[p] for p in high_peaks])
        periods = np.diff(peak_times)
        
        if len(periods) > 0:
            avg_period = np.mean(periods)
            frequency = 1 / avg_period
            print(f"Frequency = {frequency} Hz")
            return frequency
        else:
            print("Not enough data to calculate frequency.")
            return None


try:
    print("NOTE TO OUR GRADER:\n\nThis code only provides accurate when the AD2 generates a wave where there is an offset (usually equal to) the input amplitude.\nThis is so that the generated wave from the AD2 read into the unipolar MCP3008 ADC correctly, as it only reads positive bits from 0-65535")
    timer = 0
    x_points = []
    y_points = []
    freq = None
    window_size = 10000  # Adjust window size dynamically
    sma_size = 9

    

    while True:
        get_data()
        timer += 1

        if timer >= window_size:
            # smooth out the raw data using moving_avg()
            sma_raw = moving_avg(y_points, sma_size)

            # get the first derivative of the smoothed data
            first_derivative = np.gradient(sma_raw)

            # classify if the wave is square
            wave_type = eliminate_square_shape(first_derivative)

            if (wave_type == "Not Square Wave"):
                sma_first = moving_avg(first_derivative, sma_size)
                second_derivative = np.gradient(sma_first)
                second_wave_type = eliminate_square_shape(second_derivative)

                if (second_wave_type == "Square Wave"):
                    wave_type = "Triangle Wave"
                else:
                    wave_type = "Sine Wave"

            print(f"The wave is classified as: {wave_type}")

            # Get the frequency of the waveform
            freq = get_freq(x_points[:len(sma_raw)], sma_raw, wave_type)
            print()

            if freq and freq < 5:
                if wave_type == "Sine Wave":
                    window_size = 20000
                    sma_size = 15 # decrease this to get less false sines (supposed to be triangle)
                else:
                    window_size = 20000  # Increase window size for low frequencies
                    sma_size = 18
            elif freq and freq > 47: # fixing windows for high frequencies (specificially for improved triangle shape identification)
                window_size = 10000
                sma_size = 4
            else:
                window_size = 10000  # Default window size for other frequencies
                sma_size = 6


            # Reset for the next window
            x_points = []
            y_points = []
            timer = 0

finally:
    GPIO.cleanup()