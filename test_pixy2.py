#!/usr/bin/env python3
# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot

import logging
from ev3dev2.display import Display
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import TouchSensor

from time import sleep
from libs.pixy2_cam import Pixy2Cam, SignatureColor

logging.basicConfig(level=logging.INFO)

logging.info('Initializing all objects...')
# EV3 Display
lcd = Display()

# Connect ToucSensor
ts = TouchSensor(INPUT_3)

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
    
    data_cam=pixy2.find_object(1)
      
    sig =data_cam['sig']
    x = data_cam['x']
    y = data_cam['y']
    w = data_cam['w']
    h = data_cam['h']
    
    logging.info("Sig:" + str(sig))
    logging.info("X:" + str(x))
    logging.info("Y:" + str(y))
    logging.info("W:" + str(w))
    logging.info("H:" + str(h))
    logging.info("     ")
    # Scale to resolution of EV3 display:
    # Resolution Pixy2 while color tracking; (316x208)
    # Resolution EV3 display: (178x128)
    x *= 0.6
    y *= 0.6
    w *= 0.6
    h *= 0.6
    # Calculate rectangle to draw on display
    dx = int(w/2)
    dy = int(h/2)
    xa = x - dx
    ya = y + dy
    xb = x + dx
    yb = y - dy
    # Draw rectangle on display
    lcd.draw.rectangle((xa, ya, xb, yb), fill='black')
    # Update display to how rectangle
    lcd.update()
    
#turn leds Off
pixy2.turn_lamp_off()
logging.info('Shutdown...')