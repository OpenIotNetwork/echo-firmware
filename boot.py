import machine
if machine.Pin("G17", mode = machine.Pin.IN, pull = machine.Pin.PULL_UP).value() == 0:
    machine.main("noop.py")

import config
machine.WDT(timeout = config.WATCHDOG_TIMEOUT * 1000)

import pycom
pycom.heartbeat_on_boot(False)
pycom.heartbeat(False)
pycom.wifi_on_boot(False)

import network
network.WLAN().deinit()
network.Bluetooth().deinit()
network.Server().deinit()
