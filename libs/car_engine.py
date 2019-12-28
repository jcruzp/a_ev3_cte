# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot

from ev3dev2.motor import OUTPUT_C, LargeMotor, SpeedPercent
from libs.steering_wheel import SteeringWheel

class CarEngine(SteeringWheel):
    """
    Move Bot forward and backward
    """

    def __init__(self):

        SteeringWheel.__init__(self)
        self.car_engine = LargeMotor(OUTPUT_C)
     

    def move_forward(self, degrees=90):

        self.leds.set_color("LEFT", "ORANGE")
        self.car_engine.on_for_degrees(SpeedPercent(30), degrees,brake=False)
        self.leds.set_color("LEFT", "BLACK")

    def move_backward(self):

        self.leds.set_color("RIGHT", "ORANGE")
        self.car_engine.on_for_degrees(SpeedPercent(20), -90,brake=False)
        self.leds.set_color("RIGHT", "BLACK")
        
   

    