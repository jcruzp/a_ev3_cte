# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
from enum import Enum
from time import sleep
import threading

from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_B, LargeMotor, SpeedPercent

from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor

class TowerPosition(Enum):
    """
    List of wheel position
    """
    LEFT = "Left"
    RIGHT = "Right"
    CENTER = "Center"

class ScanTower():
    """
    Move turn table right and left to scan with ultrasonic sensor
    """

    def __init__(self):

        self.scan_tower = LargeMotor(OUTPUT_B)
        self.gyro_sensor = GyroSensor()
        self.gyro_sensor.reset
        self.ultrasonic_sensor = UltrasonicSensor()
        self.leds = Leds()
        self.sound = Sound()
        self.tower_position = TowerPosition.CENTER
        

    def turn_left(self):
        #0..126
        self.tower_position = TowerPosition.LEFT
        self.leds.set_color("LEFT", "RED")
        #self.scan_tower.on_for_degrees(SpeedPercent(20), -4, brake=True, block=False)
        self.scan_tower.on_for_degrees(SpeedPercent(6), -126, brake=True, block=True)
        self.leds.set_color("LEFT", "BLACK")
        #print("Angle: %4.0i Left: %10.2f" % (self.gyro_sensor.angle,self.ultrasonic_sensor.distance_centimeters))

    def turn_right(self):
        #0..-126
        self.tower_position = TowerPosition.RIGHT
        self.leds.set_color("RIGHT", "RED")
        #self.scan_tower.on_for_degrees(SpeedPercent(20), 4, brake=True, block=False)
        self.scan_tower.on_for_degrees(SpeedPercent(6), 126, brake=True, block=True)
        self.leds.set_color("RIGHT", "BLACK")
        #print("Angle: %4.0i Right: %10.2f" % (self.gyro_sensor.angle,self.ultrasonic_sensor.distance_centimeters))
        
    def print_values(self):
        while True:
            if self.tower_position != TowerPosition.CENTER:
                print("Angle: %4.0i %s: %10.2f" % (self.gyro_sensor.angle,self.tower_position,self.ultrasonic_sensor.distance_centimeters_continuous))
                sleep(0.1)

    def scan_field(self):

        #while self.gyro_sensor.angle < 90:
        #    self.turn_right()
        #    sleep(0.2)
            

        #while self.gyro_sensor.angle >= -90:
        #    self.turn_left()
        #    sleep(0.2)
            

        #while self.gyro_sensor.angle <= 0:
        #    self.turn_right()
        #    sleep(0.2)
        # Start threads
        threading.Thread(target=self.print_values, daemon=True).start()
        self.turn_right()
        self.turn_left()
        self.turn_left()
        self.turn_right()
        self.tower_position = TowerPosition.CENTER
        

        

