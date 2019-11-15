# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
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

        self.steering_wheel = MediumMotor(OUTPUT_D)
        self.leds = Leds()
        self.wheels_position = WheelsPosition.CENTER 

    def turn_left(self):

        if self.wheels_position !=  WheelsPosition.LEFT:
            self.leds.set_color("LEFT", "GREEN")
            self.steering_wheel.on_for_degrees(SpeedPercent(100), 90)
            self.leds.set_color("LEFT", "BLACK")
            self.wheels_position = WheelsPosition.LEFT

    def turn_rigth(self):

        if self.wheels_position !=  WheelsPosition.RIGHT:
            self.leds.set_color("RIGHT", "GREEN")
            self.steering_wheel.on_for_degrees(SpeedPercent(100), -90)
            self.leds.set_color("RIGHT", "BLACK")
            self.wheels_position = WheelsPosition.RIGHT
            
    def turn_center(self):
        
        if self.wheels_position ==  WheelsPosition.RIGHT:
            self.leds.set_color("RIGHT", "GREEN")
            self.steering_wheel.on_for_degrees(SpeedPercent(100), 90)
            self.leds.set_color("RIGHT", "BLACK")
        elif self.wheels_position ==  WheelsPosition.LEFT:
            self.leds.set_color("RIGHT", "GREEN")
            self.steering_wheel.on_for_degrees(SpeedPercent(100), -90)
            self.leds.set_color("RIGHT", "BLACK")
        self.wheels_position = WheelsPosition.CENTER