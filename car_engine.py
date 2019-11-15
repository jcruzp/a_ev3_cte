# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_C, LargeMotor, SpeedPercent

class CarEngine():
    """
    Move Bot forward and backward
    """

    def __init__(self):

        self.car_engine = LargeMotor(OUTPUT_C)
        self.leds = Leds()

    def move_forward(self):

        self.leds.set_color("LEFT", "ORANGE")
        self.car_engine.on_for_rotations(SpeedPercent(100), 1)
        self.leds.set_color("LEFT", "BLACK")

    def move_backward(self):

        self.leds.set_color("RIGHT", "ORANGE")
        self.car_engine.on_for_rotations(SpeedPercent(100), -1)
        self.leds.set_color("RIGHT", "BLACK")

    