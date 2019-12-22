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
from libs.gps import GPSSensor

if __name__ == '__main__':
    # Startup sequence
    gadget = GPSSensor()
    while True:
        print('Test GPS')
        data=gadget.read_latitude()
        print(data)
        data=gadget.read_longitude()
        print(data)
        #data=gadget.read_longitude()
        #print(data)
        sleep(10)