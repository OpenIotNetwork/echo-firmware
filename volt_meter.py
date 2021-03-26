# Datasheet: https://datasheets.maximintegrated.com/en/ds/MAX17043-MAX17044.pdf

import time

I2C_ADDR = 0x36
REG_VCELL = 0x02
REG_SOC = 0x04
REG_CONFIG = 0x0c

class VoltMeter():
    i2c = None

    def __init__(self, i2c):
        self.i2c = i2c

    def open(self):
        self.wakeUp()
        time.sleep(1) # Wait until first result after wakeup

    def close(self):
        self.sleep()

    def process_read(self):
        return self.voltage(), self.percentage()

    def read(i2c):
        meter = VoltMeter(i2c)
        try:
            meter.open()
            return meter.process_read()
        finally:
            meter.close()

    def voltage(self):
        data = self.readRegister(REG_VCELL)
        return (1.25 * (data >> 4)) / 1000

    def percentage(self):
        data = self.readRegister(REG_SOC)
        return ((data >> 8) + ((1 / 256) * (data & 0xFF)))

    def sleep(self):
        self.updateRegister(REG_CONFIG, 7, 1)

    def wakeUp(self):
        self.updateRegister(REG_CONFIG, 7, 0)

    def readRegister(self, reg):
        buf = self.i2c.readfrom_mem(I2C_ADDR, reg, 2)
        return ((buf[0] << 8) | buf[1])

    def writeRegister(self, reg, value):
        buf = bytearray(2)
        buf[0] = value >> 8
        buf[1] = value & 0xFF
        self.i2c.writeto_mem(I2C_ADDR, reg, buf)

    def updateRegister(self, reg, bit, value):
        buf = self.readRegister(reg)
        buf &= ~(1 << bit)
        buf |= value << bit
        self.writeRegister(reg, buf)
