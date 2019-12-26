# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot
from ev3dev2.sensor import INPUT_4
from ev3dev2.port import LegoPort

from time import sleep
from smbus import SMBus

import sys

ARDUINO_ADDRESS = 0x70

CMD_ERROR = 253

class ArduinoI2C():
    """
    Define I2C Interface protocol to arduino pro mini
    """
      
    def __init__(self):

        # Set LEGO port for arduino i2c
        lego_port = LegoPort(INPUT_4)
        lego_port.mode = 'other-i2c'
        sleep(0.5)
        # Settings for I2C (SMBus(4) for INPUT_2)
        self.lego_bus = SMBus(6)

        # HTU21D address
        self.address = ARDUINO_ADDRESS

    def read_arduino(self, command, string_length):
        """
        Connect arduino pro send command to read data
        """
        while True:
            try:
                self.lego_bus.write_byte(self.address, command)
                break
            except:
                sleep(0.1)
            
        sleep(0.01)
        while True:
            try:
                block = self.lego_bus.read_i2c_block_data(self.address, 0, string_length)
                break
            except:
                sleep(0.1)
        
        return block
        
