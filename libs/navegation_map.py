
# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot

import json
import logging

from libs.pixy2_cam import Pixy2Cam, SignatureColor
from libs.car_engine import CarEngine
from libs.scan_tower import ScanTower
from libs.color_arm import ColorArm

logging.basicConfig(level=logging.INFO)

logging.info('Initializing all objects...')

# pixel position x < MIN_LEFT tower at left
# pixel position x > MAX_RIGTH tower at right
# pixel position between MIN and MAX tower at center (pixel 156 is the center because pixy2cam is 312 x 208 resolution
MIN_LEFT = 140 
MAX_RIGHT = 172
MAX_INCHES_TOWER = 1.5

pixy2 = Pixy2Cam()

class TowerData():
    def __init__(self, color):
        self.color = color
        data_cam=pixy2.find_object( color)
        self.coord_x = data_cam['x']

    def new_position(self):
        data_cam=pixy2.find_object( self.color)
        coord_move = data_cam['x']
        return coord_move

    def pixeles_width(self):
        data_cam=pixy2.find_object( self.color)
        width = data_cam['w']
        return width
       
        

class NavegationMap():
    """
    Navegation map for Bot
    """
    
    def __init__(self):
        logging.info('Initializing tower objects...')
        self.bot = CarEngine()
        self.scan_tower = ScanTower()
        self.color_arm = ColorArm() 
                 
    
    def scan_finding_towers(self):
        
        logging.info('Turn on cam leds...')
        #turn leds On
        pixy2.turn_lamp_on()

        logging.info('Scanning tower red...')
        self.tower_red = TowerData(SignatureColor.RED) 
        logging.info('Tower red at X:' + str(tower_red.x))
        
        logging.info('Scanning tower blue...')
        self.tower_blue = TowerData(SignatureColor.BLUE) 
        logging.info('Tower blue at X:' + str(tower_blue.x))
        
        logging.info('Scanning tower yellow...')
        self.tower_yellow = TowerData(SignatureColor.YELLOW) 
        logging.info('Tower yellow at X:' + str(tower_yellow.x))
        
        logging.info('Turn off cam leds...')
        #turn leds On
        pixy2.turn_lamp_off()


    def go_tower_red(self):
        """
        |
        |
        _____
             |
             |
        """
        go_left()
        # turn scan tower right to mantain object scan active
        self.scan_tower.turn_right()
        # turn lamp on
        pixy2.turn_lamp_on()
        # move forward until tower is between range
        while tower_red.new_position()<MIN_LEFT:
            self.bot.move_forward()
        go_right()
        # turn scan tower right to mantain object scan active
        self.scan_tower.turn_left()
        # bot move until arrive at tower position
        while pixy2.object_distance(tower_red.pixeles_width())>MAX_INCHES_TOWER:
            self.bot.move_forward()
        # turn lamp on
        pixy2.turn_lamp_off()    
        #Scan and verify tower color
        print(color_arm.scan_color())
        
        
        
    def go_right(self):
        self.bot_wheel.turn_rigth()
        self.bot.move_forward()
        self.bot.move_forward()
        self.bot.move_forward()
        self.bot.move_forward()

    def go_left(self):
        self.bot_wheel.turn_left()
        self.bot.move_forward()
        self.bot.move_forward()
        self.bot.move_forward()
        self.bot.move_forward()
        
        