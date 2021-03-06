# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot
from ev3dev2.sensor import INPUT_2
from ev3dev2.port import LegoPort

from time import sleep
from smbus import SMBus

NXT_SENSOR_ADDRESS =0X4C

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
        self.address = NXT_SENSOR_ADDRESS

    def read_temperature_c(self):
        raw = self.lego_bus.read_word_data(self.address, 0) & 0xFFFF
        raw = ((raw << 8) & 0xFF00) + (raw >> 8)
        temp = (raw / 32.0) / 8.0
        return temp

    def to_fahrenheit(self, temp):
        temp = (temp * (9.0/5.0)) + 32.0
        return temp

    def read_temperature_f(self):
        temp = self.to_fahrenheit(self.read_temperature_c())
        return temp