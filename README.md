# Media Controller

This is a project to control media playback via external rotary encoder.

## Hardware

- Arduino Nano (ATMEGA328P)
- KY-040 rotary encoder or similar

## Software

Since Arduino Nano does not have HID support, this project uses a custom python script to communicate with the Arduino and control the media playback.

- Python 3 (for client)
- - [pyserial](https://pypi.org/project/pyserial/)
- - [keyboard](https://pypi.org/project/keyboard/)
- Arduino
- - [Button libary](https://github.com/madleech/Button) by Michael Adams
- - [Encoder libary](https://github.com/PaulStoffregen/Encoder) by Paul Stoffregen

## Usage

### Arduino

1. Connect the Arduino Nano to your PC via USB.
2. Connect the KY-040 rotary encoder to the Arduino Nano, make sure you conenct encoder pins to the correct board pins (see arduino file or [example pinout](#example-pinout) below).
3. In Arduino IDE, open the arduino file and select the correct board.
4. Install required Arduino libraries (see [Software](#software) section).
5. Upload the arduino file to the board.

### Python

#### Setting up the project

0. Create a virtual environment.
1. Open the python file in your favorite IDE.
2. Install requirements from the `requirements.txt` file
3. Run the python file (see `main.py --help` for available options).

> Note: you can reverse the direction of the rotary encoder by passing `--reverse` flag to the python script, just in case if your encoder is placed in the different direction.

#### Building an executable

Run the following command to build an executable file. It will be saved in the `dist` folder.

```bash
pyinstaller --noconsole --onefile --name media_control main.py
```

### Example pinout

| Rotary Encoder | Arduino Pin |
| -------------- | ----------- |
| CLK/A          | D2          |
| DT/B           | D3          |
| SW             | D4          |
| GND            | GND         |
| +              | +5V         |
