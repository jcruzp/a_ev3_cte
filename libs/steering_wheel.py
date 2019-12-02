# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot

from enum import Enum
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_D, MediumMotor, SpeedPercent

class WheelsPosition(Enum):
    """
    List of wheel position
    """
    LEFT = "Left"
    RIGHT = "Right"
    CENTER = "Center"

class SteeringWheel():
    """
    Move front wheels right and left like a steering wheel
    """

    def __init__(self):

        self.leds = Leds() 
        self.sound = Sound()
        self.steering_wheel = MediumMotor(OUTPUT_D)
        self.wheels_position = WheelsPosition.CENTER
        

    def turn_left(self):

        if self.wheels_position !=  WheelsPosition.LEFT:
            self.leds.set_color("LEFT", "GREEN")
            if self.wheels_position ==  WheelsPosition.CENTER:
                self.steering_wheel.on_for_degrees(SpeedPercent(25), -90)
            else:
                self.steering_wheel.on_for_degrees(SpeedPercent(25), -180)
            
            #self.steering_wheel.on(SpeedPercent(25)*-1)
            #self.steering_wheel.wait_until_not_moving()

            self.leds.set_color("LEFT", "BLACK")
            self.wheels_position = WheelsPosition.LEFT

    def turn_rigth(self):

        if self.wheels_position !=  WheelsPosition.RIGHT:
            self.leds.set_color("RIGHT", "GREEN")
            if self.wheels_position ==  WheelsPosition.CENTER:
                self.steering_wheel.on_for_degrees(SpeedPercent(25), 90)
            else:    
                self.steering_wheel.on_for_degrees(SpeedPercent(25), 180)
            #self.steering_wheel.on(SpeedPercent(25))
            #self.steering_wheel.wait_until_not_moving()

            self.leds.set_color("RIGHT", "BLACK")
            self.wheels_position = WheelsPosition.RIGHT
            
    def turn_center(self):
        
        if self.wheels_position ==  WheelsPosition.RIGHT:
            self.steering_wheel.on_for_degrees(SpeedPercent(25), -90)
            #self.turn_left()
        elif self.wheels_position ==  WheelsPosition.LEFT:
            self.steering_wheel.on_for_degrees(SpeedPercent(25), 90)
            #self.turn_rigth()
        self.wheels_position = WheelsPosition.CENTER