# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
from enum import Enum
from time import sleep

from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_B, LargeMotor, SpeedPercent

from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor



class ScanTower():
    """
    Move turn table right and left to scan with ultrasonic sensor
    """

    def __init__(self):

        self.scan_tower = LargeMotor(OUTPUT_B)
        self.gyro_sensor = GyroSensor()
        self.ultrasonic_sensor = UltrasonicSensor()
        self.leds = Leds()
        self.sound = Sound()
        

    def turn_left(self):
        #0..126
        self.leds.set_color("LEFT", "RED")
        self.scan_tower.on_for_degrees(SpeedPercent(20), -4, brake=True, block=False)
        self.leds.set_color("LEFT", "BLACK")
        print("Angle: %4.0i Left: %10.2f" % (self.gyro_sensor.angle,self.ultrasonic_sensor.distance_centimeters))

    def turn_right(self):
        #0..-126
        self.leds.set_color("RIGHT", "RED")
        self.scan_tower.on_for_degrees(SpeedPercent(20), 4, brake=True, block=False)
        self.leds.set_color("RIGHT", "BLACK")
        print("Angle: %4.0i Right: %10.2f" % (self.gyro_sensor.angle,self.ultrasonic_sensor.distance_centimeters))

    def scan_field(self):

        while self.gyro_sensor.angle < 90:
            self.turn_right()
            sleep(0.2)
            

        #while self.gyro_sensor.angle != 0:
        #    self.turn_left()

        while self.gyro_sensor.angle >= -90:
            self.turn_left()
            sleep(0.2)
            

        while self.gyro_sensor.angle <= 0:
            self.turn_right()
            sleep(0.2)

        

