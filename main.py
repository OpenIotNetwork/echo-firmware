FORMAT_VERSION = 1

import machine
import ubinascii
import struct
from network import LoRa
import socket
from db_meter import DBMeter
from volt_meter import VoltMeter
from led import LED
import config

led = LED()


lora = LoRa(mode = LoRa.LORAWAN, region = LoRa.EU868)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    lora.nvram_restore()

if not lora.has_joined():
    led.transmit()
    try:
        lora.join(activation = LoRa.OTAA, auth = (ubinascii.unhexlify(config.APP_EUI), ubinascii.unhexlify(config.APP_KEY)), timeout = 10000)
    except TimeoutError:
        pass

    if lora.has_joined():
        led.processing()
        voltage = VoltMeter.read()

        led.transmit()
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        s.bind(FORMAT_VERSION + 200)
        s.setblocking(True)
        s.send(struct.pack("!H", int(voltage * 100)))
        led.success(0.5)

    lora.nvram_save()
    machine.deepsleep(config.INTERVAL * 1000)

else:
    led.processing()
    result_mean, result_stdev = DBMeter.read(1000, config.SAMPLE_PERIOD)

    led.transmit()
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.bind(FORMAT_VERSION + 100)
    s.setblocking(True)
    s.send(struct.pack("!HH", int(result_mean * 100), int(result_stdev * 100)))
    led.success(0.5)

    if lora.stats().tx_counter + 1 < config.RESTART_INTERVAL / (config.INTERVAL + config.SAMPLE_PERIOD + 10): # 10 seconds added for general processing time
        lora.nvram_save()
        machine.deepsleep(config.INTERVAL * 1000)
    else:
        lora.nvram_erase()
        machine.reset()
