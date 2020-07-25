from pms import PMS
import machine
import utime
import math
import statistics

class DBMeter(PMS):
    pin = None

    def __init__(self):
        super().__init__()
        self.pin = machine.ADC().channel(pin = "P16", attn = machine.ADC.ATTN_6DB)

    def get_pp(self):
      val_min = 4096
      val_max = 0
      start = utime.ticks_ms()
      counter = 0
      while utime.ticks_ms() < start + 1:
        val = self.pin()
        counter += 1
        if val < val_min:
          val_min = val
        if val > val_max:
          val_max = val
      return val_max - val_min

    def get_avg(self, period):
        sum = 0
        for num in range(period):
            sum += self.get_pp()
        return sum / period

    def process_read(self, period, samples):
        results = []
        for num in range(samples):
            value = self.get_avg(period)
            results.append(value)
        mean = statistics.mean(results)
        stdev = statistics.stdev(results)
        return (mean, stdev)

    def read(period, samples):
        meter = DBMeter()
        try:
            meter.open()
            return meter.process_read(period, samples)
        finally:
            meter.close()
