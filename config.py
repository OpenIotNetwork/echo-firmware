# Basic config
APP_EUI = 'REMOVED'
APP_KEY = 'REMOVED'

# Advanced config (only change if you really know what you are doing!)
INTERVAL = 3600
SAMPLE_PERIOD = 30
RESTART_INTERVAL = 86400
WATCHDOG_TIMEOUT = SAMPLE_PERIOD + 30  # MUST be higher than SAMPLE_PERIOD + time for transmission
LEDS = False

#####

import machine
debug_voltage = machine.ADC().channel(pin = "P19", attn = machine.ADC.ATTN_11DB).voltage()
# Calibration: 220k resistor
if debug_voltage > 1250 and debug_voltage < 1750:
    INTERVAL = 60
    LEDS = False
# Test: Closed
elif debug_voltage > 3000:
    INTERVAL = 60
    LEDS = True
