#!/usr/bin/env python3
from ev3dev2.display import Display
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor

from time import sleep
from pixy2_cam import Pixy2Cam #, DataCam


# EV3 Display
lcd = Display()

# Connect ToucSensor
ts = TouchSensor(INPUT_1)

pixy2=Pixy2Cam()

#turn leds On
pixy2.set_leds(1)

# Read and display data until TouchSensor is pressed
while not ts.value():
    # Clear display
    lcd.clear()
    
    data_cam=pixy2.find_object(1)
     
    # sig =data_cam.sig
    # x = data_cam.x
    # y = data_cam.y
    # w = data_cam.w
    # h =data_cam.h
    
    sig =data_cam['sig']
    x = data_cam['x']
    y = data_cam['y']
    w = data_cam['w']
    h = data_cam['h']
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
    
#turn leds On
pixy2.set_leds()