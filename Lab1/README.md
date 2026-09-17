# Lab 1 – Using GPIO as Input and Output

**Objective:** Use the Raspberry Pi's GPIO pins for digital input (push button) and digital
output (RGB LEDs, 7-segment display) to build a two-way pedestrian/traffic stoplight system,
implemented twice — once with polling and once with interrupts.

## System behavior

- Traffic light 2 (RGB LED) stays **green** by default.
- Pressing the button turns traffic light 2 **blue**, blinks it 3 times, then **red**.
- Once traffic light 2 is red, traffic light 1 turns **green** and a 7-segment display
  counts down from 9 to 0.
- When the countdown reaches 4, traffic light 1 flashes **blue** until the countdown hits 0.
- At 0, traffic light 1 turns **red** and traffic light 2 returns to **green**.
- A 20-second cooldown prevents the button from re-triggering the cycle immediately.

## Files

- [`Csce462-500_Group1_Lab1_polling.py`](Csce462-500_Group1_Lab1_polling.py) — reads the
  button state with `GPIO.input()` inside a continuously running loop (polling).
- [`Csce462-500_Group1_Lab1_interrupt.py`](Csce462-500_Group1_Lab1_interrupt.py) — same
  system, but uses `GPIO.add_event_detect()` / `GPIO.add_event_callback()` to react to a
  falling-edge interrupt on the button pin instead of continuously polling it.
- [`Lab 1 Instructions.pdf`](Lab%201%20Instructions.pdf) — original lab assignment/instructions.
- [`Csce 462-500 _ Lab Report 1 _ Group 1 - Segun.docx.pdf`](Csce%20462-500%20%20_%20%20Lab%20Report%201%20%20_%20%20Group%201%20-%20Segun.docx.pdf) —
  submitted lab report with circuit diagram, code, and answers to the lab questions
  (CPU clock speed, GPIO logic-level voltages, RPi vs. PC, polling vs. interrupts,
  hardware vs. software interrupts).

## Hardware

Raspberry Pi 3, 2x common-cathode RGB LED, push button, 7-segment display, resistors.
