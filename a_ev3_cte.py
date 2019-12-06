#!/usr/bin/env python3
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
#
# You may not use this file except in compliance with the terms and conditions
# set forth in the accompanying LICENSE.TXT file.
#
# THESE MATERIALS ARE PROVIDED ON AN "AS IS" BASIS. AMAZON SPECIFICALLY DISCLAIMS, WITH
# RESPECT TO THESE MATERIALS, ALL WARRANTIES, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING
# THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

from ev3dev2.led import Leds
from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MediumMotor, MoveTank,
                           SpeedPercent)

#from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sound import Sound
#from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.sensor.lego import UltrasonicSensor

from ev3dev2.sensor.lego import ColorSensor

import json
import logging
import random
import threading
import time
from enum import Enum

from agt import AlexaGadget

from libs.color_arm import ColorArm
from libs.steering_wheel import SteeringWheel
from libs.car_engine import CarEngine
from libs.scan_tower import ScanTower

# Set the logging level to INFO to see messages from AlexaGadget
logging.basicConfig(level=logging.INFO)


# class Direction(Enum):
#     """
#     The list of directional commands and their variations.
#     These variations correspond to the skill slot values.
#     """
#     FORWARD = ['forward', 'forwards', 'go forward']
#     BACKWARD = ['backward', 'backwards', 'go backward']
#     LEFT = ['left', 'go left']
#     RIGHT = ['right', 'go right']
#     STOP = ['stop', 'brake', 'halt']


# class Command(Enum):
#     """
#     The list of preset commands and their invocation variation.
#     These variations correspond to the skill slot values.
#     """
#     MOVE_CIRCLE = ['circle', 'move around']
#     MOVE_SQUARE = ['square']
#     SENTRY = ['guard', 'guard mode', 'sentry', 'sentry mode']
#     PATROL = ['patrol', 'patrol mode']
#     FIRE_ONE = ['cannon', '1 shot', 'one shot']
#     FIRE_ALL = ['all shots', 'all shot']


# class EventName(Enum):
#     """
#     The list of custom event name sent from this gadget
#     """
#     SENTRY = "Sentry"
#     PROXIMITY = "Proximity"
#     SPEECH = "Speech"

class EventName(Enum):
    """
    The list of custom event name sent from this gadget
    """
    ARRIVE_TOWER = "at_tower"
    ARRIVE_BASE = "at_base" 
    TEMPERATURE = "temperature"
    HUMIDITY ="humidity"
    COLOR = "color"
    GPS = "gps"
    ALLCONDITIONS = "all_conditions"

class MindstormsGadget(AlexaGadget):
    """
    A Mindstorms gadget that can perform bi-directional interaction with an Alexa skill.
    """

    def __init__(self):
        """
        Performs Alexa Gadget initialization routines and ev3dev resource allocation.
        """
        super().__init__()

        # Robot state
        self.sentry_mode = False
        self.patrol_mode = False

        # Connect two large motors on output ports B and C
        self.drive = MoveTank(OUTPUT_B, OUTPUT_C)
        self.weapon = MediumMotor(OUTPUT_A)
        self.sound = Sound()
        self.leds = Leds()
        #self.ir = InfraredSensor()
        self.us = UltrasonicSensor()

        # Start threads
        threading.Thread(target=self._patrol_thread, daemon=True).start()
        threading.Thread(target=self._proximity_thread, daemon=True).start()

    def on_connected(self, device_addr):
        """
        Gadget connected to the paired Echo device.
        :param device_addr: the address of the device we connected to
        """
        self.leds.set_color("LEFT", "GREEN")
        self.leds.set_color("RIGHT", "GREEN")
        print("{} connected to Echo device".format(self.friendly_name))

    def on_disconnected(self, device_addr):
        """
        Gadget disconnected from the paired Echo device.
        :param device_addr: the address of the device we disconnected from
        """
        self.leds.set_color("LEFT", "BLACK")
        self.leds.set_color("RIGHT", "BLACK")
        print("{} disconnected from Echo device".format(self.friendly_name))

    def on_custom_mindstorms_gadget_control(self, directive):
        """
        Handles the Custom.Mindstorms.Gadget control directive.
        :param directive: the custom directive with the matching namespace and name
        """
        try:
            payload = json.loads(directive.payload.decode("utf-8"))
            print("Control payload: {}".format(payload))
            control_type = payload["type"]
        
            if control_type == "read_conditions" :
               self._read_conditions(payload["botposition"], payload["condition"]) 
            
            if control_type == "return_base" :
                self._return_base() 
                
            if control_type == "verify_color" :
                self._verify_color(payload["botposition"]) 
                
            if control_type == "exploring_towers" :
                self._exploring_towers(payload["towerColorA"],payload["towerColorB"])  
                
            """
            if control_type == "move"

                # Expected params: [direction, duration, speed]
                self._move(payload["direction"], int(
                    payload["duration"]), int(payload["speed"]))

            if control_type == "command":
                # Expected params: [command]
                self._activate(payload["command"])
            """
        except KeyError:
            print("Missing expected parameters: {}".format(directive))

    def _read_ambiente_temperature(self):
        self._send_event(EventName.TEMPERATURE, {
                              'speechOut': "Temperature at " + botposition + " is 10 degrees F"}) 

    def _read_relative_humidity(self):
        self._send_event(EventName.HUMIDITY, {
                              'speechOut': "Relative humidity at " + botposition + " is 20%"}) 

    def _read_gps_position(self):
        self._send_event(EventName.GPS, {
                              'speechOut': "GPS coordinates at " + botposition + " are latitude 10 degrees and longitude 30 degrees"})   
    
    def _read_conditions(self, botposition, condition):
        if (condition == "ambient temperature"):
            self._read_ambiente_temperature()
        
        if (condition == "relative humidity"):
            self._read_relative_humidity()    
                
        if (condition == "GPS position"):
            self._read_gps_position() 

        if (condition == "all conditions"):
            self._send_event(EventName.ALLCONDITIONS, {
                              'speechOut': "Reading all tower conditions "})
            self._read_ambiente_temperature()
            self._read_relative_humidity()
            self._read_gps_position()  

                    
    def _return_base(self):
        self._send_event(EventName.ARRIVE_BASE, {
                              'speechOut': "Robot arrive at base"})
        
    def _verify_color(self, botposition):
        self._send_event(EventName.HUMIDITY, {
                              'speechOut': "Color verified for " + botposition})  
        
    def _exploring_towers(self, towerColorA, towerColorB):
        print(towerColorA.capitalize())
        print(towerColorB.capitalize())
        self._send_event(EventName.ARRIVE_TOWER, {
                              'speechOut': "Robot arrive xxx tower." })
        
                

    # def _move(self, direction, duration: int, speed: int, is_blocking=False):
    #     """
    #     Handles move commands from the directive.
    #     Right and left movement can under or over turn depending on the surface type.
    #     :param direction: the move direction
    #     :param duration: the duration in seconds
    #     :param speed: the speed percentage as an integer
    #     :param is_blocking: if set, motor run until duration expired before accepting another command
    #     """
    #     print("Move command: ({}, {}, {}, {})".format(
    #         direction, speed, duration, is_blocking))
    #     if direction in Direction.FORWARD.value:
    #         self.drive.on_for_seconds(SpeedPercent(speed), SpeedPercent(
    #             speed), duration, block=is_blocking)

    #     if direction in Direction.BACKWARD.value:
    #         self.drive.on_for_seconds(
    #             SpeedPercent(-speed), SpeedPercent(-speed), duration, block=is_blocking)

    #     if direction in (Direction.RIGHT.value + Direction.LEFT.value):
    #         self._turn(direction, speed)
    #         self.drive.on_for_seconds(SpeedPercent(speed), SpeedPercent(
    #             speed), duration, block=is_blocking)

    #     if direction in Direction.STOP.value:
    #         self.drive.off()
    #         self.patrol_mode = False

    # def _activate(self, command, speed=50):
    #     """
    #     Handles preset commands.
    #     :param command: the preset command
    #     :param speed: the speed if applicable
    #     """
    #     print("Activate command: ({}, {})".format(command, speed))
    #     if command in Command.MOVE_CIRCLE.value:
    #         self.drive.on_for_seconds(SpeedPercent(
    #             int(speed)), SpeedPercent(5), 12)

    #     if command in Command.MOVE_SQUARE.value:
    #         for i in range(4):
    #             self._move("right", 2, speed, is_blocking=True)

    #     if command in Command.PATROL.value:
    #         # Set patrol mode to resume patrol thread processing
    #         self.patrol_mode = True

    #     if command in Command.SENTRY.value:
    #         self.sentry_mode = True
    #         self._send_event(EventName.SPEECH, {
    #                          'speechOut': "Sentry mode activated"})

    #         # Perform Shuffle posture
    #         self.drive.on_for_seconds(SpeedPercent(80), SpeedPercent(-80), 0.2)
    #         time.sleep(0.3)
    #         self.drive.on_for_seconds(SpeedPercent(-40), SpeedPercent(40), 0.2)

    #         self.leds.set_color("LEFT", "YELLOW", 1)
    #         self.leds.set_color("RIGHT", "YELLOW", 1)

    #     if command in Command.FIRE_ONE.value:
    #         print("Fire one")
    #         self.weapon.on_for_rotations(SpeedPercent(100), 3)
    #         self._send_event(EventName.SENTRY, {'fire': 1})
    #         self.sentry_mode = False
    #         print("Sent sentry event - 1 shot, alarm reset")
    #         self.leds.set_color("LEFT", "GREEN", 1)
    #         self.leds.set_color("RIGHT", "GREEN", 1)

    #     if command in Command.FIRE_ALL.value:
    #         print("Fire all")
    #         self.weapon.on_for_rotations(SpeedPercent(100), 10)
    #         self._send_event(EventName.SENTRY, {'fire': 3})
    #         self.sentry_mode = False
    #         print("sent sentry event - 3 shots, alarm reset")
    #         self.leds.set_color("LEFT", "GREEN", 1)
    #         self.leds.set_color("RIGHT", "GREEN", 1)

    # def _turn(self, direction, speed):
    #     """
    #     Turns based on the specified direction and speed.
    #     Calibrated for hard smooth surface.
    #     :param direction: the turn direction
    #     :param speed: the turn speed
    #     """
    #     if direction in Direction.LEFT.value:
    #         self.drive.on_for_seconds(SpeedPercent(0), SpeedPercent(speed), 2)

    #     if direction in Direction.RIGHT.value:
    #         self.drive.on_for_seconds(SpeedPercent(speed), SpeedPercent(0), 2)

    def _send_event(self, name: EventName, payload):
        """
        Sends a custom event to trigger a sentry action.
        :param name: the name of the custom event
        :param payload: the sentry JSON payload
        """
        self.send_custom_event('Custom.Mindstorms.Gadget', name.value, payload)

    def _proximity_thread(self):
        """
        Monitors the distance between the robot and an obstacle when sentry mode is activated.
        If the minimum distance is breached, send a custom event to trigger action on
        the Alexa skill.
        """
        count = 0
        while True:
            while self.sentry_mode:
                #distance = self.ir.proximity
                distance = self.us.distance_centimeters_continuous
                print("Proximity: {}".format(distance))
                count = count + 1 if distance < 10 else 0
                if count > 3:
                    print("Proximity breached. Sending event to skill")
                    self.leds.set_color("LEFT", "RED", 1)
                    self.leds.set_color("RIGHT", "RED", 1)

                    self._send_event(EventName.PROXIMITY, {
                                     'distance': distance})
                    self.sentry_mode = False

                time.sleep(0.2)
            time.sleep(1)

    def _patrol_thread(self):
        """
        Performs random movement when patrol mode is activated.
        """
        while True:
            while self.patrol_mode:
                print("Patrol mode activated randomly picks a path")
                direction = random.choice(list(Direction))
                duration = random.randint(1, 5)
                speed = random.randint(1, 4) * 25

                while direction == Direction.STOP:
                    direction = random.choice(list(Direction))

                # direction: all except stop, duration: 1-5s, speed: 25, 50, 75, 100
                self._move(direction.value[0], duration, speed)
                time.sleep(duration)
            time.sleep(1)


if __name__ == '__main__':
    # Startup sequence
    gadget = MindstormsGadget()
    gadget.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))
    gadget.leds.set_color("LEFT", "GREEN")
    gadget.leds.set_color("RIGHT", "GREEN")

    # Gadget main entry point
    gadget.main()

    # Shutdown sequence
    gadget.sound.play_song((('E5', 'e'), ('C4', 'e')))
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")
