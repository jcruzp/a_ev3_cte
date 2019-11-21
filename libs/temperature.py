# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.port import LegoPort

from time import sleep
from smbus import SMBus
from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_C, LargeMotor, SpeedPercent

class TemperatureSensor():
    """
    Read temperature using NXT Temperature sensor
    """

    def __init__(self):
          
        # Set LEGO port for NXT Temp sensor
        lego_port = LegoPort(INPUT_2)
        lego_port.mode = 'other-i2c'
        sleep(0.5)
        # Settings for I2C (SMBus(4) for INPUT_2)
        self.lego_bus =  SMBus(4)
        # LM75 address
        self.address = 0x4C

    def read_temperature_c(self):
        #block = self.lego_bus.read_i2c_block_data(self.address, 0, 1) 
        # 
        # 
        # data = bus.read_i2c_block_data(0x48, 0)
        #        TempMSB = data[0]
        #        TempLSB = data[1]
        # Read I2C data and calculate temperature
        raw = self.lego_bus.read_word_data(self.address, 0) & 0xFFFF
        raw = ((raw << 8) & 0xFF00) + (raw >> 8)
        return (raw / 32.0) / 8.0

    def to_fahrenheit(self, temp):
		return (temp * (9.0/5.0)) + 32.0


    