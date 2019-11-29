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
from libs.color_arm import ColorArm, ColorScanOptions
from libs.temperature import TemperatureSensor

# pixel position x < MIN_LEFT tower at left
# pixel position x > MAX_RIGTH tower at right
# pixel position between MIN and MAX tower at center (pixel 156 is the center because pixy2cam is 312 x 208 resolution
MIN_LEFT = 140
MAX_RIGHT = 172
# Max inches from bot to arrives tower
MAX_INCHES_TOWER = 1.5

pixy2 = Pixy2Cam()
logging.basicConfig(level=logging.INFO)


class TowerData():
    """
    Handles data for each tower
    """

    def __init__(self, color):
        logging.info('Initializing tower data...')
        self.color = color
        data_cam = pixy2.find_object(color)
        self.coord_x = data_cam['x']
        self.temperature = 0

    def new_position(self):
        """
        Center position of object in camera image
        """
        data_cam = pixy2.find_object(self.color)
        return data_cam['x']

    def pixeles_width(self):
        """
        Tower pixeles width in image
        """
        data_cam = pixy2.find_object(self.color)
        return data_cam['w']


class NavegationMap():
    """
    Navegation map for Bot
    """

    def __init__(self, tower_order_list=[ColorScanOptions.RED, ColorScanOptions.BLUE, ColorScanOptions.YELLOW]):
        logging.info('Initializing navegation map ...')
        self.bot = CarEngine()
        self.scan_tower = ScanTower()
        self.color_arm = ColorArm()
        self.steps_left = 0
        self.steps_right = 0
        self.steps_forward = 0
        self.tower_order_list = tower_order_list
        self.temperature = TemperatureSensor()

    def scan_finding_towers(self):
        """
        Initial scan position for all towers
        """
        logging.info('Turn on cam leds...')
        # turn leds On
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
        # turn leds Off
        pixy2.turn_lamp_off()

    def go_until_near_tower(self, tower_color):
        """
        Move forward until arrive at tower position
        """
        logging.info('Arriving tower color ' + tower_color.color)
        self.steps_forward = 0
        # bot move until arrive at tower position
        while pixy2.object_distance(tower_color.pixeles_width()) > MAX_INCHES_TOWER:
            self.bot.move_forward()
            self.steps_forward += 1
        # turn lamp off
        pixy2.turn_lamp_off()
        # Scan and verify tower color
        logging.info('Verifying tower color ...' + self.color_arm.scan_color())
        # print(color_arm.scan_color())

    def go_right(self, backward=False):
        """
        Turn right moving forward or backward
        """
        self.bot.turn_rigth()
        if (backward):
            logging.info('Going right backward...')
            self.bot.move_backward()
            self.bot.move_backward()
            self.bot.move_backward()
            self.bot.move_backward()
        else:
            logging.info('Going right forward...')
            self.bot.move_forward()
            self.bot.move_forward()
            self.bot.move_forward()
            self.bot.move_forward()

    def go_left(self, backward=False):
        """
        Turn left moving forward or backward
        """
        self.bot.turn_left()
        if (backward):
            logging.info('Going left backward...')
            self.bot.move_backward()
            self.bot.move_backward()
            self.bot.move_backward()
            self.bot.move_backward()
        else:
            logging.info('Going left forward...')
            self.bot.move_forward()
            self.bot.move_forward()
            self.bot.move_forward()
            self.bot.move_forward()

    def go_red_tower(self):
        """
        |
        |
        ^___<
        Move to red tower at left position
        """
        logging.info('Going to red tower...')
        self.go_left()
        # turn scan tower right to mantain object scan active
        self.scan_tower.turn_right()
        # turn lamp on
        pixy2.turn_lamp_on()
        # move forward until tower is between range
        while self.tower_red.new_position() < MIN_LEFT:
            self.bot.move_forward()
            self.steps_left += 1
        self.go_right()
        # turn scan tower right to mantain object scan active
        self.scan_tower.turn_left()
        self.go_until_near_tower(self.tower_red)

    def return_from_red_tower(self):
        """
        Return back to the base from red tower
        """
        logging.info('Return back to base from red tower...')
        while self.steps_forward > 0:
            self.bot.move_backward()
            self.steps_forward -= 1
        self.go_right(backward=True)
        while self.steps_left > 0:
            self.bot.move_backward()
            self.steps_left -= 1
        self.go_left(backward=True)
        logging.info('Arriving to base...')

    def go_blue_tower(self):
        """
        |
        |
        ^        
        Move to blue tower at center position
        """
        logging.info('Going to blue tower...')
        # turn lamp on
        pixy2.turn_lamp_on()
        self.go_until_near_tower(self.tower_blue)

    def return_from_blue_tower(self):
        """
        Return back to base from blue tower
        """
        logging.info('Return back to base from blue tower...')
        while self.steps_forward > 0:
            self.bot.move_backward()
            self.steps_forward -= 1
        logging.info('Arriving to base...')

    def go_yellow_tower(self):
        """
            |
            |
        >___^
        Move to yellow tower at right position
        """
        logging.info('Going to yellow tower...')
        self.go_right()
        # turn scan tower right to mantain object scan active
        self.scan_tower.turn_left()
        # turn lamp on
        pixy2.turn_lamp_on()
        # move forward until tower is between range
        while self.tower_yellow.new_position() > MAX_RIGHT:
            self.bot.move_forward()
            self.steps_right += 1
        self.go_left()
        # turn scan tower right to mantain object scan active
        self.scan_tower.turn_right()
        self.go_until_near_tower(self.tower_yellow)

    def return_from_yellow_tower(self):
        """
        Return back to base from yellow tower
        """
        logging.info('Return back to base from yellow tower...')
        while self.steps_forward > 0:
            self.bot.move_backward()
            self.steps_forward -= 1
        self.go_left(backward=True)
        while self.steps_right > 0:
            self.bot.move_backward()
            self.steps_right -= 1
        self.go_right(backward=True)
        logging.info('Arriving to base...')

    def exploring_towers(self):
        """
        Go to each tower and exploring using all sensors
        """
        logging.info('Begin exploring towers ...')
        # Scan all initial towers position
        self.scan_finding_towers()
        # Go and scan each tower in established order
        for tower in self.tower_order_list:
            if tower == ColorScanOptions.RED:
                self.go_red_tower()
                # Scan all we need using sensors
                self.tower_red.temperature = self.temperature.read_temperature_f()
                self.return_from_red_tower()
            elif tower == ColorScanOptions.BLUE:
                self.go_blue_tower()
                # Scan all we need
                self.tower_blue.temperature = self.temperature.read_temperature_f()
                self.return_from_blue_tower()
            elif tower == ColorScanOptions.YELLOW:
                self.go_yellow_tower()
                # Scan all we need
                self.tower_yellow.temperature = self.temperature.read_temperature_f()
                self.return_from_yellow_tower()
