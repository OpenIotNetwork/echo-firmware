from pms import PMS
import machine
import utime

class VoltMeter(PMS):
    RESISTOR_NETWORK_FACTOR = 2

    pin = None

    def __init__(self):
        super().__init__()
        self.pin = machine.ADC().channel(pin = "P17", attn = machine.ADC.ATTN_11DB)

    def process_read(self):
        cycles = 10
        interval = 50
        sum = 0
        for num in range(cycles):
            sum += self.pin.voltage()
            utime.sleep_ms(interval)
        return (sum / cycles) * self.RESISTOR_NETWORK_FACTOR / 1000

    def read():
        meter = VoltMeter()
        try:
            meter.open()
            return meter.process_read()
        finally:
            meter.close()
