# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_C, MediumMotor, SpeedPercent

class SteeringWheel():
    """
    Move front wheels right and left like a steering wheel
    """

    def __init__(self):

        self.steering_wheel = MediumMotor(OUTPUT_C)
        self.leds = Leds()

    def turn_left(self):

        self.leds.set_color("LEFT", "GREEN")
        self.steering_wheel.on_for_rotations(SpeedPercent(100), 1)
        self.leds.set_color("LEFT", "BLACK")

    def turn_rigth(self):

        self.leds.set_color("RIGHT", "GREEN")
        self.steering_wheel.on_for_rotations(SpeedPercent(100), -1)
        self.leds.set_color("RIGHT", "BLACK")


