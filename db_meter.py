import time
import utime
import statistics
import machine

INTERVAL = 500

class DBMeter():
    modbus = None
    modbus_psu = None

    def __init__(self, modbus, modbus_psu):
        self.modbus = modbus
        self.modbus_psu = modbus_psu

    def open(self):
        self.modbus_psu.hold(False)
        self.modbus_psu.value(1)
        time.sleep(3) # Wait for IC to be ready for results

    def close(self):
        self.modbus_psu.value(0)
        self.modbus_psu.hold(True)

    def process_read(self, period):
        results = []
        now = utime.ticks_ms()
        stop = now + period
        while now < stop:
            now = utime.ticks_ms()
            results.append(self.modbus.read_holding_registers(0x01, 0x00, 0x01, True)[0] / 10)
            utime.sleep_ms(INTERVAL - (utime.ticks_ms() - now))
        mean = statistics.mean(results)
        stdev = statistics.stdev(results)
        return (mean, stdev)

    def read(modbus, modbus_psu, period):
        meter = DBMeter(modbus, modbus_psu)
        try:
            meter.open()
            return meter.process_read(period)
        finally:
            meter.close()
