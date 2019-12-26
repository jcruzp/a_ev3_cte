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
from libs.humidity import HumiditySensor

if __name__ == '__main__':
    # Startup sequence
    gadget = HumiditySensor()
    while True:
        print('Test Humidity')
        print(gadget.read_humidity())
        #print ('{0:0.2f}'.format(gadget.check_crc(0x4E85,0x6B)) )
        sleep(1)
    
    