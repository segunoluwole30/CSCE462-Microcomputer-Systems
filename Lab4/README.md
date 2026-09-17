# Lab 4 – Inertial Measurement Units (IMU)

**Objective:** Interface an MPU6050 IMU (accelerometer/gyroscope) with a Raspberry Pi over
I2C and use accelerometer data to build a step-counting pedometer.

## Assignment

Read live acceleration data from the MPU6050, calibrate against a resting baseline, and
count steps in real time as a person wearing the sensor walks.

## Files

- [`gyro_cleaned_full.py`](gyro_cleaned_full.py) — a two-phase pedometer:
  - **Calibration phase:** takes one acceleration reading while the device is at rest and
    computes the magnitude of that vector as a baseline.
  - **Movement phase:** polls acceleration continuously for up to 60 seconds (or 52 steps),
    computes the magnitude of each new reading, and counts a step whenever the magnitude
    deviates more than ±10% from the calibrated baseline, with a short debounce delay to
    avoid double-counting a single step.
- [`Csce 462-500 _ Lab Report 4 _ Group 1 - Segun Oluwole.pdf`](Csce%20462-500%20%20_%20%20Lab%20Report%204%20%20_%20%20Group%201%20-%20Segun%20Oluwole.pdf) —
  submitted lab report with circuit diagram, code walkthrough, and answers to the lab
  questions (sensor polling rate, filtering approach, step-counting algorithm and measured
  accuracy — 30 counted vs. 33 actual steps, ~91% accuracy).

## Hardware

Raspberry Pi 3, MPU6050 IMU (accelerometer + gyroscope, I2C).
