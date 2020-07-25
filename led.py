import pycom
import time
import config

class LED:
    SUCCESS = 0x00ff00
    ERROR = 0xff0000
    TRANSMIT = 0x0000ff
    PROCESSING = 0xffff00

    def set(self, color, timeout = None):
        if not config.LEDS:
            return

        pycom.rgbled(color)

        if timeout is not None:
            time.sleep(timeout)

    def success(self, timeout = None):
        self.set(self.SUCCESS, timeout)

    def error(self, timeout = None):
        self.set(self.ERROR, timeout)

    def transmit(self, timeout = None):
        self.set(self.TRANSMIT, timeout)

    def processing(self, timeout = None):
        self.set(self.PROCESSING, timeout)
