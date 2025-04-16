# Audio Equalizer

A comprehensive audio equalizer with various effects, built using Python and Tkinter.

## Features

- 10-band equalizer
- Volume control
- Binaural audio effects
- 3D surround sound
- 8D audio effect
- Bass boost
- Reverb
- Audio visualization
- Import and export audio files

## Requirements

- Python 3.7 or higher
- Required libraries: tkinter, numpy, scipy, pydub, simpleaudio, soundfile, matplotlib

## Installation

1. Clone this repository
2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

## Usage

1. Click "Open Audio File" to load an audio file (MP3, WAV, OGG, or FLAC)
2. Adjust the equalizer sliders to modify frequency responses
3. Enable various audio effects and adjust their parameters:
   - 3D Surround: Creates spatial separation between audio elements
   - 8D Audio: Rotates audio between left and right channels
   - Binaural Effect: Generates binaural beats for specific frequencies
   - Bass Boost: Enhances low frequency response
   - Reverb: Adds room echo effects
4. Use the "Play" button to hear the modifications in real-time
5. Save the processed audio using the "Save As" button

## Notes

This application works offline without internet connection and is compatible with Windows 10.