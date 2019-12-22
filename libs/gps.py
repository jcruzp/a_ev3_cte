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

from libs.arduino_i2c import ArduinoI2C
import sys
import time

GPS_ADDRESS = 0x70

class GPSCommands(Enum):
    """
    List of GPS Commands
    """
    LATITUDE = 2
    LAT = 3
    LONGITUDE = 4
    LONG = 5
    
 
class GPSSensor(ArduinoI2C):
    """
    Read GPS latitude and longitude
    """

    def __init__(self):
          
        ArduinoI2C.__init__(self)


    def read_latitude(self):
        #while True:
        latitude=self.read_arduino(7,8)
        latitudestr=''.join(map(chr,latitude))
        #    if 254 not in latitude: 
        #        break 
        #    else:
        #        sleep(1)
         
        print(latitude)
        #while True: 
        lat = self.read_arduino(5,1)
        latstr=''.join(map(chr,lat))
        #    if 254 not in lat: 
        #        break 
        #    else:
        #        sleep(1)
           
        print(lat)
        return latitudestr + latstr
    
    def read_longitude(self):
        while True:
            longitude=''.join(map(chr,self.read_arduino(GPSCommands.LONGITUDE.value,12)))
            if longitude != "error": break
        while True:    
            lon=''.join(map(chr,self.read_arduino(GPSCommands.LONG.value,1)))
            if lon != "error": break
        return longitude + lon