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
    
    nav_map = NavegationMap(tower_order_list=['red'])
    nav_map.exploring_towers()
    logging.info('Shutdown...')


    
    
    
    
    