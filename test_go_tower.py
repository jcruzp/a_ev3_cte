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

from libs.pixy2_cam import Pixy2Cam
from libs.steering_wheel import SteeringWheel 
from libs.car_engine import CarEngine

if __name__ == '__main__':
    
    
    pixy2=Pixy2Cam()

    logging.info('Turn on cam leds...')
    #turn leds On
    pixy2.turn_lamp_on()

    logging.info('Scanning field search color towers...')
    # Read and display data until TouchSensor is pressed
    #data_cam=pixy2.find_object(2)
    #data_cam=pixy2.find_object(2)
    while not ts.value():
    # Clear display
    lcd.clear()
    
    data_cam=pixy2.find_object(SignatureColor.RED)
      
    sig =data_cam['sig']
    x = data_cam['x']
    y = data_cam['y']
    w = data_cam['w']
    h = data_cam['h']
    
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
    
    
    
    