# MIDI Mixer

## What is it?

A GUI application that allows you to map a MIDI device's Control Change messages to control PulseAudio sink input (application) volume.

Inspired by https://www.midi-mixer.com/, I decided to make this ugly version for Linux using the following:
- tkinter
- [mido](https://pypi.org/project/mido/ "mido") (uses [python-rtmidi](https://pypi.org/project/python-rtmidi/ "python-rtmidi")?)
- [pulsectl](https://pypi.org/project/pulsectl/ "pulsectl")

## Installation

1. Install Python
2. Download the source code
3. Navigate into the project folder
4. Run `pip install -r requirements.txt` in a terminal

## Usage

With the application running:
1. Select your device from the first combobox
2. Hook one of its controls by pressing the button and moving it on your device
3. Select the sink input (application) which you want to control
4. ???
5. Profit

## Yet to be implemented

### Persistent settings

Currently, controls need to be hooked every time the application is started

### Profiles

As you probably guessed, no persistence also means no savable profiles at this time.

------------
## Miscellaneous info

This is the first actually useful project that I have done. If you notice some kind of Python convention mistake, please let me know or submit a pull request. I guess all kinds of pull requests and issues are also welcome, I haven't really collaborated on GitHub before and have mixed feelings about putting/having this here at all.

I know Python isn't the obvious and most definitely not the prettiest choice for a GUI, but it is the language I want to focus on. It would be cool to see this project inspire someone to make a modern-looking version of this in another language.
