# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 15:45:37 2023

@author: leyu3109
"""

import os

os.environ['BLINKA_MCP2221']  = '1'

import time
import board
#from busio import I2C
import digitalio
import numpy as np
from time import sleep
import string
import random
from adafruit_bus_device import i2c_device

os.environ['BLINKA_MCP2221']  = '1'
device_address = 0x18
controlreg = 0xfffe
statusreg = 0xfffc
interrupt_eng_reg = 0xfffa
interrupt_flg_reg = 0xfff8
crc_result_reg = 0xfff6
crc_len_reg = 0xfff4
watchdog_con_reg = 0xfff0
version_reg = 0xffee
ndefID_reg = 0xffec
hostresponse = 0xffea
ndefblocklength_reg = 0xffe8
nedfoffset_reg = 0xffe6
buffer_start = 0xffe4
swtx_reg = 0xffde
sw1sw2_reg = 0xffda
bufferini_add = 0x0000
bufferend_add = 0x0bb7

target = digitalio.DigitalInOut(board.G1)
target.direction = digitalio.Direction.OUTPUT  # Configure as an output

standard = digitalio.DigitalInOut(board.G0)
standard.direction = digitalio.Direction.OUTPUT  # Configure as an output

def pulse_generator():
    target.value = 1
    time.sleep(0.01)
    target.value = 0

def pulse_generator_standard():
    standard.value = 1
    time.sleep(0.01)
    standard.value = 0
pulse_generator()    