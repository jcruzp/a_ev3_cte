#!/usr/bin/env python3
# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot

import os
import sys
import time
import logging

from time import sleep
from libs.temperature import TemperatureSensor

if __name__ == '__main__':
    # Startup sequence
    gadget = TemperatureSensor()
    while True:
        print('Temperature: {0:0.2f} *C'.format(gadget.read_temperature_c()))
        sleep(1)
    
    