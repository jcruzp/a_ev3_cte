
# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot

import json
import logging

from libs.pixy2_cam import Pixy2Cam, SignatureColor
from libs.car_engine import CarEngine
from libs.steering_wheel import SteeringWheel

logging.basicConfig(level=logging.INFO)

logging.info('Initializing all objects...')

# pixel position x < MIN_LEFT tower at left
# pixel position x > MAX_RIGTH tower at right
# pixel position between MIN and MAX tower at center (pixel 156 is the center because pixy2cam is 312 x 208 resolution
MIN_LEFT = 140 
MAX_RIGHT = 172

class TowerData():
    def __init__(self, color, x):
        self.color = color
        self.coord_x = x
        

class NavegationMap():
    """
    Navegation map for Bot
    """
    
    def __init__(self):
        logging.info('Initializing tower objects...')
        self.pix2cam = Pixy2Cam()
        self.bot = CarEngine()
        self.bot_wheel = SteeringWheel()
        self.tower_1 = TowerData(SignatureColor.NONE,0)
        self.tower_2 = TowerData(SignatureColor.NONE,0)
        self.tower_3 = TowerData(SignatureColor.NONE,0)
        
        
    
    def scan_finding_towers(self):
        
        pixy2=Pixy2Cam()

        logging.info('Turn on cam leds...')
        #turn leds On
        pixy2.turn_lamp_on()

        logging.info('Scanning tower red...')
        self.tower_1.color=SignatureColor.RED
        data_cam=pixy2.find_object( self.tower_1.color)
        self.tower_1.x=data_cam['x']
        logging.info('Tower red at :' + str(tower_1.x))
        
        logging.info('Scanning tower blue...')
        self.tower_2.color=SignatureColor.BLUE
        data_cam=pixy2.find_object( self.tower_2.color)
        self.tower_2.x=data_cam['x'] 
        logging.info('Tower blue at :' + str(tower_2.x))
        
        logging.info('Scanning tower yellow...')
        self.tower_3.color=SignatureColor.YELLOW
        data_cam=pixy2.find_object( self.tower_3.color)
        self.tower_3.x=data_cam['x']
        logging.info('Tower yellow at :' + str(tower_3.x))
        
        logging.info('Turn off cam leds...')
        #turn leds On
        pixy2.turn_lamp_off()
        
        
    def go_right(self):
        self.bot.move_forward()
        self.bot_wheel.turn_rigth()
        self.bot.move_forward()
        self.bot.move_forward()
        
        