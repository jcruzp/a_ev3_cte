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
        # Settings for I2C (SMBus(3) for INPUT_4)
        self.lego_bus =  SMBus(4)
        # Make sure the same address is set in Pixy2
        self.address = 0x4C

    def read_temperature(self):
        block = self.lego_bus.read_i2c_block_data(self.address, 0, 1)  
        return block


    