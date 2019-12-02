#!/usr/bin/env python3
# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot

import os
import sys
from time import sleep
import logging

from libs.navegation_map import NavegationMap

if __name__ == '__main__':
    
    nav_map = NavegationMap(tower_order_list=['Blue','Red'])
    nav_map.exploring_towers()
    #nav_map.go_right()
    #nav_map.go_left()
    
    logging.info('Shutdown...')


    
    
    
    
    