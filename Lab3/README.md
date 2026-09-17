# Lab 3 – Interfacing an Analog to Digital Converter (ADC) with a Microcontroller

**Objective:** Learn to read analog sensor/signal data into a Raspberry Pi (which has no
built-in analog input) using an MCP3008 10-bit ADC over SPI, then use that data to build a
simple software oscilloscope.

## Assignment

Build a simple oscilloscope using the Raspberry Pi + MCP3008 that can:
1. **Recognize a wave** — classify an incoming analog signal as square, sine, or triangle.
2. **Characterize a wave** — compute and print the signal's frequency.

## Files

- [`oscilloscope_polling.py`](oscilloscope_polling.py) — samples the ADC channel
  continuously (`get_data()`), smooths the samples with a moving average
  (`moving_avg()`), classifies the waveform shape by looking at flat regions/abrupt slope
  changes in the 1st and 2nd derivatives (`eliminate_square_shape()`, used to distinguish
  square vs. triangle vs. sine), computes frequency from threshold crossings or peak
  spacing (`get_freq()`), and dynamically adjusts the sampling window/smoothing size
  based on the detected frequency range.
- [`Lab 3 Instructions.pdf`](Lab%203%20Instructions.pdf) — original lab assignment/instructions.
- [`Csce 462-500 _ Lab Report 3 _ Group 1 - Segun.docx.pdf`](Csce%20462-500%20%20_%20%20Lab%20Report%203%20%20_%20%20Group%201%20-%20Segun.docx.pdf) —
  submitted lab report with circuit diagram, code walkthrough, and answers to the lab
  questions (SPI vs. I2C, ADC types and MCP3008's tradeoffs, sampling rate, self-interference
  when generating and reading a wave on the same Pi, noise filtering method).

## Hardware

Raspberry Pi 3, MCP3008 10-bit ADC (SPI), Analog Discovery 2 as the signal source,
resistors.
