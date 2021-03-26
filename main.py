FORMAT_VERSION = 1

import machine

from network import LoRa
import socket
import ubinascii
import struct

from uModBus.serial import Serial as ModbusSerial
from machine import Pin
from db_meter import DBMeter

from machine import I2C
from volt_meter import VoltMeter

from led import LED

import config

led = LED()

lora = LoRa(mode = LoRa.LORAWAN, region = LoRa.EU868, adr = True)

i2c = I2C()
modbus = ModbusSerial(1, pins = ("P3", "P4"))
modbus_psu = Pin("P8", mode = machine.Pin.OUT)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    lora.nvram_restore()

if not lora.has_joined():
    led.transmit()
    try:
        lora.join(activation = LoRa.OTAA, auth = (ubinascii.unhexlify(config.APP_EUI), ubinascii.unhexlify(config.APP_KEY)), timeout = 10000, dr = 0)
    except TimeoutError:
        pass

    if lora.has_joined():
        led.processing()
        # TODO Should round before sending - just dropping precision otherwise?
        voltage, percentage = VoltMeter.read(i2c)

        led.transmit()
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        s.bind(FORMAT_VERSION + 200)
        s.setblocking(True)
        s.send(struct.pack("!HH", int(voltage * 100), int(percentage * 100)))
        led.success(0.5)

    lora.nvram_save()
    machine.deepsleep(int(config.INTERVAL * 1000))

else:
    led.processing()
    # TODO Should round before sending - just dropping precision otherwise?
    result_mean, result_stdev = DBMeter.read(modbus, modbus_psu, config.SAMPLE_PERIOD * 1000)

    led.transmit()
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.bind(FORMAT_VERSION + 100)
    s.setblocking(True)
    s.send(struct.pack("!HH", int(result_mean * 100), int(result_stdev * 100)))
    led.success(0.5)

    if lora.stats().tx_counter + 1 < config.RESTART_INTERVAL / (config.INTERVAL + config.SAMPLE_PERIOD + 10): # 10 seconds added for general processing time
        lora.nvram_save()
        machine.deepsleep(int(config.INTERVAL * 1000))
    else:
        lora.nvram_erase()
        machine.reset()
