# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
from enum import Enum

from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_A, MediumMotor, SpeedPercent


from ev3dev2.sensor.lego import ColorSensor

class ArmPosition(Enum):
    """
    List of color arm position
    """
    CONTRACT = "Contract"
    STRETCH = "Stretch"

class ColorScanOptions(Enum):
    """
    List of colors that could be scaned
    """
    NONE = "NoColor"
    RED = "Red"
    YELLOW = "Yellow"
    BLUE = "Blue"

class ColorArm():
    """
    Stretch the color arm to scan color tower and contract it at end 
    """

    def __init__(self):

        self.leds = Leds()
        self.arm_position = ArmPosition.CONTRACT
        self.color_arm = MediumMotor(OUTPUT_A)
        self.color_sensor = ColorSensor()
        self.color_scaned = ColorScanOptions.NONE

    def strech_arm(self):

        if self.arm_position in ArmPosition.CONTRACT:
            self.leds.set_color("LEFT", "YELLOW")
            self.color_arm.on_for_rotations(
                SpeedPercent(100), 1, brake=True, block=True)
            self.leds.set_color("LEFT", "BLACK")
            self.arm_position = ArmPosition.STRETCH

    def contract_arm(self):

        if self.arm_position in ArmPosition.STRETCH:
            self.leds.set_color("RIGHT", "YELLOW")
            self.color_arm.on_for_rotations(
                SpeedPercent(100), -1, brake=True, block=True)
            self.leds.set_color("RIGHT", "BLACK")
            self.arm_position = ArmPosition.CONTRACT
            
    @property
    def scan_color(self):
        self.strech_arm()
        self.color_scaned = self.color_sensor.color_name
        self.contract_arm
        return self.color_scaned