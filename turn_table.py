# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
from enum import Enum

from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_B, LargeMotor, SpeedPercent

from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor

class TurnTablel():
    """
    Move turn table right and left to scan with ultrasound 
    """

    def __init__(self):

        self.turn_table = LargeMotor(OUTPUT_B)
        self.gyro_sensor = GyroSensor()
        self.ultrasonic_sensor = UltrasonicSensor()
        self.leds = Leds()

    def turn_left(self):

        self.leds.set_color("LEFT", "RED")
        self.turn_table.on_for_rotations(SpeedPercent(100), 1)
        self.leds.set_color("LEFT", "BLACK")

    def turn_rigth(self):

        self.leds.set_color("RIGHT", "RED")
        self.turn_table.on_for_rotations(SpeedPercent(100), -1)
        self.leds.set_color("RIGHT", "BLACK")

    def scan_field(self):

        while self.gyro_sensor.angle != 90:
            self.turn_right()

        #while self.gyro_sensor.angle != 0:
        #    self.turn_left()

        while self.gyro_sensor.angle != -90:
            self.turn_left()

        while self.gyro_sensor.angle !=0:
            self.turn_right()

        

