# Basic config
APP_EUI = 'REMOVED'
APP_KEY = 'REMOVED'

# Advanced config (only change if you really know what you are doing!)
INTERVAL = 3600
SAMPLE_PERIOD = 30
RESTART_INTERVAL = 86400
WATCHDOG_TIMEOUT = SAMPLE_PERIOD + 30  # MUST be higher than SAMPLE_PERIOD + time for transmission
LEDS = False
CALIBRATION_MODE = True

#####

import machine
TEST_MODE = True if machine.Pin("P21", mode = machine.Pin.IN, pull = None).value() == 1 else False
if TEST_MODE:
    INTERVAL = 60
    LEDS = True
    if CALIBRATION_MODE:
        LEDS = False
