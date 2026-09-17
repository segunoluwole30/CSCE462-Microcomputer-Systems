# Lab 2 – Digital to Analog Converter (DAC) with a Microcontroller

**Objective:** Learn to generate analog waveforms from a Raspberry Pi using an MCP4725
12-bit DAC over I2C, and use those waveforms to build a button-driven function generator.

## Assignment

Build a function generator: pressing an external push button prompts the user (via the
command line) for a waveform shape (`sq` / `sin` / `tri`), a maximum output voltage (0–VCC),
and a frequency (up to 50 Hz). The Raspberry Pi then continuously outputs that waveform
through the DAC until the button is pressed again, at which point it prompts for new
parameters.

## Files

- [`function_generator.py`](function_generator.py) — implements `square_wave()`,
  `sin_wave()`, and `triangle_wave()`, each computing the correct DAC raw value
  (0–4095, corresponding to 0–3.3V) at every time step, plus `button_logic()` which polls
  the button (GPIO26) and drives the interactive prompt/output loop.
- [`Lab 2 Instructions.pdf`](Lab%202%20Instructions.pdf) — original lab assignment/instructions.
- [`Segun's Copy of Csce 462-500 _ Lab Report 2 _ Group 1.docx.pdf`](Segun's%20Copy%20of%20Csce%20462-500%20%20_%20%20Lab%20Report%202%20%20_%20%20Group%201.docx.pdf) —
  submitted lab report with circuit diagram, code walkthrough, and answers to the lab
  questions (max digital output frequency, signal noise, PWM-to-analog conversion,
  max frequency per waveform shape, function-generator state machine design).

## Hardware

Raspberry Pi 3, MCP4725 12-bit DAC (I2C), push button, resistor, Analog Discovery 2 /
oscilloscope for verifying the output waveform.
