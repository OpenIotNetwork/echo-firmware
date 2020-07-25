import machine
import utime

class PMS:
    SETTLE_PERIOD = 0.5

    pms_pin = None

    def __init__(self):
        self.pms_pin = machine.Pin("P20", mode = machine.Pin.OUT)

    def open(self):
        self.pms_pin.hold(False)
        self.pms_pin.value(1)
        utime.sleep(self.SETTLE_PERIOD)

    def close(self):
        self.pms_pin.value(0)
        self.pms_pin.hold(True)
