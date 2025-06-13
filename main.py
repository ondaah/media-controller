import time
import argparse
import datetime

import serial
import keyboard


class EncoderHandler:
    """
    :param com_port: The serial port to use, i.e. `"COM10"`
    :param baud_rate: The baud rate to use, i.e. `9600`
    :param timeout: The timeout to use for reading from the serial port, i.e. `0.1`
    :param reverse: Whether to reverse the direction of the encoder, i.e. `False`
    :param click_timeout: The timeout to use for clicking the button, i.e. `0.6`
    """

    def __init__(
        self,
        com_port: str,
        baud_rate: int = 9600,
        timeout: float = 0.1,
        reverse: bool = False,
        click_timeout: float = 0.6,
    ):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.reverse = reverse
        self.click_timeout = click_timeout

        self._serial = serial.Serial(
            self.com_port, self.baud_rate, timeout=self.timeout
        )

        self._last_position: int = 0
        self._button_state: int = 0
        self._button_pressed_at: float = 0.0

    @classmethod
    def _log(cls, message: str):
        print(
            "[{}] {}".format(
                datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), message
            )
        )

    def _handle_encoder(self, position: int):
        if position == self._last_position:
            return

        _up = self.reverse if position > self._last_position else not self.reverse

        if self._button_state == 1:
            self._log("next track" if _up else "previous track")
            keyboard.send("next track" if _up else "previous track")
        else:
            self._log("volume up" if _up else "volume down")
            keyboard.send("volume up" if _up else "volume down")

        self._last_position = position

    def _handle_button(self, state: int):
        if self._button_state == state:
            return

        if state == 1:
            self._button_pressed_at = time.time()
        else:
            self._log(
                "pressed for {:.2f} sec.".format(time.time() - self._button_pressed_at)
            )
            if time.time() - self._button_pressed_at <= self.click_timeout:
                self._log("play/pause media")
                keyboard.send("play/pause media")

        self._button_state = state

    def start(self):
        try:
            while True:
                line = self._serial.readline().decode().strip()
                if len(line) == 0:
                    continue
                self._log(line)

                if line.startswith("e"):
                    self._handle_encoder(int(line[1:]))
                elif line.startswith("b"):
                    self._handle_button(int(line[1:]))
        except KeyboardInterrupt:
            self._log("Exiting")
        finally:
            self._serial.close()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--com",
        type=str,
        default="COM10",
        help="The serial port to use, i.e. `COM10`",
    )
    parser.add_argument(
        "--baud",
        type=int,
        default=9600,
        help="The baud rate to use, i.e. `9600`",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Whether to reverse the direction of the encoder, i.e. `False`",
    )
    parser.add_argument(
        "--click-timeout",
        type=float,
        default=0.6,
        help="The timeout to use for clicking the button, i.e. `0.6`",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        handler = EncoderHandler(
            com_port=args.com,
            baud_rate=args.baud,
            reverse=args.reverse,
            click_timeout=args.click_timeout,
        )
        print("Listening on COM port", args.com)
        handler.start()
    except serial.SerialException:
        print(f'Unable to open COM port "{args.com}"')


if __name__ == "__main__":
    main()
