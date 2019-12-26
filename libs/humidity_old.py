# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot
from ev3dev2.sensor import INPUT_4
from ev3dev2.port import LegoPort

from time import sleep
from enum import IntEnum
from smbus import SMBus

import sys

import time

HTDU21D_ADDRESS = 0x40

SHIFTED_DIVISOR = 0x988000

class HTU21D_COMMANDS(IntEnum):
    TRIGGER_TEMP_MEASURE_HOLD=0xE3
    TRIGGER_HUMD_MEASURE_HOLD=0xE5
    TRIGGER_TEMP_MEASURE_NOHOLD=0xF3
    TRIGGER_HUMD_MEASURE_NOHOLD=0xF5
    WRITE_USER_REG=0xE6
    READ_USER_REG=0xE7
    SOFT_RESET=0xFE

class HumiditySensorOld():
    """
    Read humidity using HTU21D humidity sensor
    """

    def __init__(self):
          
        # Set LEGO port for HTU21D sensor
        lego_port = LegoPort(INPUT_4)
        lego_port.mode = 'other-i2c'
        sleep(0.5)
        # Settings for I2C (SMBus(4) for INPUT_2)
        self.lego_bus =  SMBus(6)
        
        # HTU21D address
        self.address = 0x40


    def read(self):
        """
        Read humidity from sensor and verify checksum
        """
                     
        #self.lego_bus.write_byte(self.address, 0xF5)
        #time.sleep(0.2)
        block=0
        rawhumidity=0
        counter=0
        toRead=0
        while counter < 10 and toRead != 3:
            self.lego_bus.write_byte(self.address, 0xFE)
            self.lego_bus.write_byte(self.address, 0xF5)
            sleep(1)
            
            try:
                block = self.lego_bus.read_i2c_block_data(self.address, 0, 3)
                print (block)
                rawhumidity = (( block[0] << 8) | block[1])
                print (rawhumidity)
            except:
                print("Error inesperado:", sys.exc_info()[0])
            counter +=1
        

        rh=999 # if invalid checksum return error value
        if (self.check_crc(rawhumidity, block[2]) == 0):  #Verify the checksum         
            #rawhumidity &= 0xFFFC
            print (rawhumidity)
            tempRH = rawhumidity / 65536.0
            rh = -6.0 + (125.0 * tempRH)
        return rh


    def check_crc(self,message_from_sensor, check_value_from_sensor):
        """
        Verify if read data is ok
        Test cases from datasheet:
        message = 0xDC, checkvalue is 0x79
        message = 0x683A, checkvalue is 0x7C
        message = 0x4E85, checkvalue is 0x6B
        """
        remainder = message_from_sensor << 8 #Pad with 8 bits because we have to add in the check value
        remainder |= check_value_from_sensor #Add on the check value

        divsor = SHIFTED_DIVISOR

        for i in range(0, 16): #Operate on only 16 positions of max 24. The remaining 8 are our remainder and should be zero when we're done.
            if ((remainder &  1 << (23 - i)) > 0): #Check if there is a one in the left position
                remainder ^= divsor
            divsor >>= 1 #Rotate the divsor max 16 times so that we have 8 bits left of a remainder
        
        return remainder




  