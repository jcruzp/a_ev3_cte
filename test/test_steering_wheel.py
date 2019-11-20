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

from ..libs.steering_wheel import SteeringWheel 

if __name__ == '__main__':
    # Startup sequence
    gadget = SteeringWheel()
    #gadget.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")
    gadget.turn_rigth()
    sleep(5)
    gadget.turn_center()
    sleep(5)
    gadget.turn_left()
    sleep(5)
    gadget.turn_center()
    
    
    
    