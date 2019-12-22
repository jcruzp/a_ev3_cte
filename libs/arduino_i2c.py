# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot
from ev3dev2.sensor import INPUT_2
from ev3dev2.port import LegoPort

from time import sleep
from enum import Enum
from smbus import SMBus

import sys

import time


class ArduinoI2C():
    """
    Define I2C Interface protocol to arduino pro mini
    """

    def __init__(self):

        # Set LEGO port for arduino i2c
        lego_port = LegoPort(INPUT_2)
        lego_port.mode = 'other-i2c'
        sleep(0.5)
        # Settings for I2C (SMBus(4) for INPUT_2)
        self.lego_bus = SMBus(4)

        # HTU21D address
        self.address = 0x70

    def read_arduino(self, command, string_length):
        self.lego_bus.write_byte(self.address, command)
        sleep(0.01)
        block = self.lego_bus.read_i2c_block_data(self.address, 0, string_length)
        return block
        

'''  def read_arduino(self, command, string_length):
        """
        Connect arduino pro send command to read data
        """
        i = command
        while i+1 > 0:
            try:
                data = self.lego_bus.read_byte(self.address)
                sleep(0.01)
                i -= 1
            except:
                sleep(0.01)
        sleep(0.03)
        try:
            data = self.lego_bus.read_byte(self.address)
        except:
            data = 0
        if (command == data):
            sleep(0.01)
            data = self.lego_bus.read_byte(self.address)
            if data == 35:
                sleep(0.01)
                block = self.lego_bus.read_i2c_block_data(
                    self.address, 0, string_length)
               # if 101 in block:
                #    return  [101, 114, 114, 111, 114]
                # else:
                return block
            else:
                print("No # char")
        else:
            print("data != type_read")
        return [101, 114, 114, 111, 114]
 '''
