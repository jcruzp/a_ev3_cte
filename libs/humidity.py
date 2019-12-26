# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot
from libs.arduino_i2c import ArduinoI2C

CMD_GET_HUMIDITY = 0x07

class HumiditySensor(ArduinoI2C):
    """
    Read Humidity from HTU21D sensor with Arduino Pro Mini 
    HTU21D is no an I2C compatible with EV3 because of that uses Arduino 
    """

    def __init__(self):

        ArduinoI2C.__init__(self)

    def read_humidity(self):
        humidity = self.read_arduino(CMD_GET_HUMIDITY, 8)
        humiditystr = ''.join(map(chr, humidity))
        return humiditystr
