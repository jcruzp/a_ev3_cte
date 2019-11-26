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

from libs.car_engine import CarEngine 

if __name__ == '__main__':
    # Startup sequence
    gadget = CarEngine()
    gadget.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")
    gadget.turn_rigth()
    #gadget.move_forward(720)
    gadget.move_forward()
    gadget.move_forward()
    gadget.move_forward()
    gadget.move_forward()
    gadget.turn_center()
    gadget.turn_left()
    gadget.move_forward()
    gadget.move_forward()
    gadget.move_forward()
    gadget.move_forward()
    gadget.turn_center()
    #gadget.move_forward(540)
    #gadget.move_forward()
    #gadget.move_forward()
    #gadget.move_forward()
    #gadget.move_forward()
    #gadget.move_forward()
    
    
    
    
    