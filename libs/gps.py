# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot
from ev3dev2.sensor import INPUT_2
from ev3dev2.port import LegoPort

from time import sleep
from enum import Enum, IntEnum
from smbus import SMBus

from libs.arduino_i2c import ArduinoI2C
import sys
import time




class GPSCommands(IntEnum):
    """
    List of GPS Commands
    """
    LATITUDE = 2
    LAT = 3
    LONGITUDE = 4
    LON = 5


DATA_ERROR = "Error"

GPS_NO_DATA = 254

class GPSSensor(ArduinoI2C):
    """
    Read GPS latitude and longitude
    """

    def __init__(self):

        ArduinoI2C.__init__(self)

    def read_latitude(self):
        latitude = self.read_arduino(GPSCommands.LATITUDE, 12)
        latitudestr = ''.join(map(chr, latitude))

        print(latitude)

        lat = self.read_arduino(GPSCommands.LAT, 1)
        latstr = ''.join(map(chr, lat))

        print(lat)
        return DATA_ERROR if (GPS_NO_DATA in latitude) or (GPS_NO_DATA in lat) else latitudestr + latstr

    def read_longitude(self):
        longitude = self.read_arduino(GPSCommands.LONGITUDE, 12)
        longitudestr = ''.join(map(chr, longitude))

        print(longitude)

        lon = self.read_arduino(GPSCommands.LON, 1)
        lonstr = ''.join(map(chr, lon))

        print(lon)
        return DATA_ERROR if (GPS_NO_DATA in longitude) or (GPS_NO_DATA in lon) else longitudestr + lonstr
