# System requirements:
# a. When the button has not been pressed, traffic light 2 stays green
# b. When the button is pressed, traffic light 2 turns to blue, blinks 3  times, then
# turns red.
# c. When Traffic light 2 turns red, traffic light 1 becomes green and the countdown
# panel begins to count down from 9 to 0, in seconds. (In the real world it would
# be longer)
# d. When countdown reaches 4, traffic light 1 flashes with blue light until time 0.
# e. When countdown reaches 0, traffic light 1 becomes red, traffic light 2
# becomes green.
# f. When the button is pressed once there will be a 20 seconds cooldown to be
# able to make another valid press.

# Implementation requirements: implement the system in both two ways as below
# a. Read press button state using the polling method (always checking for a change in the value)
# b. Read press button state using the interrupt method (only checking when the value is changed)

import time

import RPi.GPIO as GPIO


# LABEL ALL THE BCM GPIO PIN NUMBERS AND THE CORRESPONDING COMPONENT
# traffic light 1:
red1 = 18
green1 = 23
blue1 = 24

# traffic light 2:
red2 = 25
green2 = 12
blue2 = 16

# seven segment:
segE = 4
segD = 17
segC = 27
# skipping the decimal point
segG = 22
segF = 5
segA = 13
segB = 6

# button
button = 26



# GPIO SETTINGS
GPIO.setmode(GPIO.BCM)

GPIO.setup(red1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(blue1, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(red2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(blue2, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(segA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(segB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(segC, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(segD, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(segE, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(segF, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(segG, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)



# SEVEN SEGMENT DISPLAY HELPER DICTIONARIES
num = {
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '0': (1, 1, 1, 1, 1, 1, 0),
    '1': (0, 1, 1, 0, 0, 0, 0),
    '2': (1, 1, 0, 1, 1, 0, 1),
    '3': (1, 1, 1, 1, 0, 0, 1),
    '4': (0, 1, 1, 0, 0, 1, 1),
    '5': (1, 0, 1, 1, 0, 1, 1),
    '6': (1, 0, 1, 1, 1, 1, 1),
    '7': (1, 1, 1, 0, 0, 0, 0),
    '8': (1, 1, 1, 1, 1, 1, 1),
    '9': (1, 1, 1, 0, 0, 1, 1)
}

seg_map = {0: segA, 1: segB, 2: segC, 3: segD, 4: segE, 5: segF, 6: segG}


# TRAFFIC LIGHT 1 LED HELPER FUNCTIONS
def traffic1_off():
  GPIO.output(red1, GPIO.LOW)
  GPIO.output(blue1, GPIO.LOW)
  GPIO.output(green1, GPIO.LOW)


def traffic1_red():
  GPIO.output(red1, GPIO.HIGH)
  GPIO.output(blue1, GPIO.LOW)
  GPIO.output(green1, GPIO.LOW)


def traffic1_blue():
  GPIO.output(red1, GPIO.LOW)
  GPIO.output(blue1, GPIO.HIGH)
  GPIO.output(green1, GPIO.LOW)


def traffic1_green():
  GPIO.output(red1, GPIO.LOW)
  GPIO.output(blue1, GPIO.LOW)
  GPIO.output(green1, GPIO.HIGH)


# TRAFFIC LIGHT 2 LED HELPER FUNCTIONS
def traffic2_off():
  GPIO.output(red2, GPIO.LOW)
  GPIO.output(blue2, GPIO.LOW)
  GPIO.output(green2, GPIO.LOW)


def traffic2_red():
  GPIO.output(red2, GPIO.HIGH)
  GPIO.output(blue2, GPIO.LOW)
  GPIO.output(green2, GPIO.LOW)


def traffic2_blue():
  GPIO.output(red2, GPIO.LOW)
  GPIO.output(blue2, GPIO.HIGH)
  GPIO.output(green2, GPIO.LOW)


def traffic2_green():
  GPIO.output(red2, GPIO.LOW)
  GPIO.output(blue2, GPIO.LOW)
  GPIO.output(green2, GPIO.HIGH)


def traffic2_blue_blinking():
  # blink 3 times
  for _ in range(3):
    traffic2_blue()
    time.sleep(.1)
    traffic2_off()
    time.sleep(1)


def seg_on():
  # The seven segment display counts down from 9 to 0
  for i in range(9, -1, -1):

    # when the countdown is at 4, 3, 2, or 1, traffic light 1 will blink blue
    if (i == 4 or i == 3 or i == 2 or i == 1):  # TIME IS 4s
      traffic1_blue()
      time.sleep(.1)
      traffic1_off()
      time.sleep(.1)

    # when the countdown reaches 0, 
    # traffic light 1 turns red, and traffic light 2 turns green
    if i == 0:  # TIME IS 0s
      traffic1_red()
      traffic2_green()

    # Enables and disables the proper segments depending on the countdown value
    for j in range(7):
      if num[str(i)][j] == 1:
        GPIO.output(seg_map[j], GPIO.HIGH)
      else:
        GPIO.output(seg_map[j], GPIO.LOW)
    time.sleep(1)

  # Turn off the display after countdown is completed
  for j in range(7):
    GPIO.output(seg_map[j], GPIO.LOW)


def cycle_rgb1():
  # Cycles through red, green, blue LEDs for testing purposes
  traffic1_red()
  time.sleep(1)

  traffic1_blue()
  time.sleep(1)

  traffic1_green()
  time.sleep(1)

  traffic1_off()
  time.sleep(1)


def cycle_rgb2():
  # Cycles through red, green, blue LEDs for testing purposes
  traffic2_red()
  time.sleep(1)

  traffic2_blue()
  time.sleep(1)

  traffic2_green()
  time.sleep(1)

  traffic2_off()
  time.sleep(1)


def button_callback(button):
  # This is the actions that should take place after the button is pressed 
  # This will only trigger if the button is pressed

  time.sleep(0.1)
  if GPIO.input(button) == GPIO.LOW:
    # ~ print("button is pressed")
    traffic2_blue()
    traffic2_blue_blinking()
    traffic2_red()
    traffic1_green()
    seg_on()
    time.sleep(5)
  else:
    # ~ print("button is not pressed")
    traffic2_green()
    traffic1_red()  #WE ADDED THIS


def main():
  # TESTING THE COLORS
  # cycle_rgb1()
  # cycle_rgb2()

  print("starting")
  try:
    # When the python script is started, these actions occur

    time.sleep(1)
    traffic2_green()
    traffic1_red()  #WE ADDED THIS

    # Created an event detection for the falling edge of the button, specifying functionality in button_callback()
    GPIO.add_event_detect(button,
                          GPIO.FALLING,
                          callback=button_callback,
                          bouncetime=50)
    
    # Need a continuous while loop to check for button activity
    while True:
      pass

  finally:
    # Clean the GPIO pin settings for a future run, no matter how the script ended
    GPIO.cleanup()


if __name__ == "__main__":
  main()

GPIO.cleanup()
