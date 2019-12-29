#!/usr/bin/env python3
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
#
# You may not use this file except in compliance with the terms and conditions
# set forth in the accompanying LICENSE.TXT file.
#
# THESE MATERIALS ARE PROVIDED ON AN "AS IS" BASIS. AMAZON SPECIFICALLY DISCLAIMS, WITH
# RESPECT TO THESE MATERIALS, ALL WARRANTIES, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING
# THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
#
# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot
from libs.arduino_i2c import ArduinoI2C

from ev3dev2.led import Leds
from ev3dev2.sound import Sound

import json
import logging
import random
import threading
from time import sleep
from enum import Enum

from agt import AlexaGadget

from libs.color_arm import ColorArm
from libs.navegation_map import NavegationMap
from libs.temperature import TemperatureSensor
from libs.humidity import HumiditySensor
from libs.gps import GPSSensor

# Set the logging level to INFO to see messages from AlexaGadget
logging.basicConfig(level=logging.INFO)


class DirectiveName(Enum):
    """
    List of directives send by Alexa Skill
    """
    READ_CONDITIONS = "read_conditions"
    RETURN_BASE = "return_base"
    VERIFY_COLOR = "verify_color"
    EXPLORING_TOWERS = "exploring_towers"


class EventName(Enum):
    """
    The list of custom event name sent from this gadget
    """
    GOING_TOWER = "going_tower"
    RETURN_BASE = "return_base"
    ARRIVE_TOWER = "at_tower"
    ARRIVE_TOWER_AUTO = "at_tower_auto"
    ARRIVE_BASE = "at_base"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    COLOR = "color"
    GPS = "gps"
    ALLCONDITIONS = "all_conditions"


class ConditionName(Enum):
    """
    List of all conditios to read at tower
    """
    AMBIENTE_TEMPERATURE = "ambient temperature"
    RELATIVE_HUMIDITY = "relative humidity"
    GPS_POSITION = "GPS position"
    ALL_CONDITIONS = "all conditions"


class RobotPosition(Enum):
    """
    List of robot positions 
    """
    ROBOT_AT_BASE = "base"
    ROBOT_AT_RED_TOWER = "red tower"
    ROBOT_AT_BLUE_TOWER = "blue tower"


class MindstormsGadget(AlexaGadget):
    """
    A Mindstorms gadget that can perform bi-directional interaction with an Alexa skill.
    """

    def __init__(self):
        """
        Performs Alexa Gadget initialization routines and ev3dev resource allocation.
        """
        super().__init__()

        # Robot initial position
        self.botposition = RobotPosition.ROBOT_AT_BASE.value

        self.sound = Sound()
        self.leds = Leds()

        self.nav_map = NavegationMap()

        # Start threads
        #threading.Thread(target=self._patrol_thread, daemon=True).start()
        #threading.Thread(target=self._proximity_thread, daemon=True).start()

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
            # Retrieve directive
            control_type = payload["type"]
            # Retrieve robot position
            self.botposition = payload["botposition"]

            # Process all directives
            if control_type == DirectiveName.READ_CONDITIONS.value:
                self._read_conditions(payload["condition"])

            if control_type == DirectiveName.RETURN_BASE.value:
                self._return_base()

            if control_type == DirectiveName.VERIFY_COLOR.value:
                self._verify_color()

            if control_type == DirectiveName.EXPLORING_TOWERS.value:
                self._exploring_towers(
                    payload["towerColorA"], payload["towerColorB"])

        except KeyError:
            print("Missing expected parameters: {}".format(directive))

    def _read_ambiente_temperature(self):
        """
        Read temperature at tower using temperature sensor
        """
        temperature = TemperatureSensor()
        self._send_event(EventName.TEMPERATURE.value, {
            'speechOut': "Temperature at " + self.botposition + " is {0:0.2f} ".format(temperature.read_temperature_f()) + " degrees fahrenheit"})

    def _read_relative_humidity(self):
        """
        Read humidity at tower using humidity sensor
        """
        humidity = HumiditySensor()
        self._send_event(EventName.HUMIDITY.value, {
            'speechOut': "Relative humidity at " + self.botposition + " is {0:0.2f} ".format(humidity.read_humidity()) + " percent"})

    def _read_gps_position(self):
        """
        Read GPS latitude and longitude coordinates
        """
        #gpsdata = GPSSensor()
        #self._send_event(EventName.GPS.value, {
        #    'speechOut': "GPS coordinates at " + self.botposition + " are latitude " + gpsdata.read_latitude().strip() + " and longitude " + gpsdata.read_longitude() })
        self._send_event(EventName.GPS.value, {
            'speechOut': "GPS coordinates at " + self.botposition + " are, latitude 1015.5234 degrees N,  and longitude 6757.8689 degrees W"})
        
    def _read_all_conditions(self):
        """
        Read all conditions
        """   
        temperature = TemperatureSensor()
        humidity = HumiditySensor()
        gpsdata = GPSSensor()
        #self._send_event(EventName.ALLCONDITIONS.value, {
        #    'speechOut': "At " + self.botposition + " Temperature is {0:0.2f} ".format(temperature.read_temperature_f()) + " degrees fahrenheit.,,," +
        #                 "Relative humidity is {0:0.2f} ".format(humidity.read_humidity()) + " percent.,,," +
        #                 "GPS coordinates are latitude, " + gpsdata.read_latitude().strip() + " and longitude, " + gpsdata.read_longitude() })
        self._send_event(EventName.ALLCONDITIONS.value, {
            'speechOut': "At " + self.botposition + " Temperature is {0:0.2f} ".format(temperature.read_temperature_f()) + " degrees fahrenheit.,,," +
                         "Relative humidity is {0:0.2f} ".format(humidity.read_humidity()) + " percent.,,," +
                         "GPS coordinates are latitude, 1015.5245 degrees N, and longitude, 6757.8654 degrees W" })

    def _read_conditions(self, condition):
        """
        Read one or all conditions at each tower
        """
        if (condition == ConditionName.AMBIENTE_TEMPERATURE.value):
            self._read_ambiente_temperature()

        if (condition == ConditionName.RELATIVE_HUMIDITY.value):
            self._read_relative_humidity()

        if (condition == ConditionName.GPS_POSITION.value):
            self._read_gps_position()
       
        if (condition == ConditionName.ALL_CONDITIONS.value):
           self._read_all_conditions()

    def _return_base(self):
        """
        Robot return to base from current tower
        """
        if (self.botposition == RobotPosition.ROBOT_AT_RED_TOWER.value):
            self.nav_map.return_from_red_tower()
        if (self.botposition == RobotPosition.ROBOT_AT_BLUE_TOWER.value):
            self.nav_map.return_from_blue_tower()
        self._send_event(EventName.ARRIVE_BASE.value, {
            'speechOut': "Explorer arrive at base",
            'botPosition': RobotPosition.ROBOT_AT_BASE.value})

    def _verify_color(self):
        """
        Verify scanned color at each tower
        """
        color_arm = ColorArm()
        tower_color = color_arm.scan_color()
        self._send_event(EventName.COLOR.value, {
            'speechOut': "The scanned color at " + self.botposition + " is " + tower_color})

    def _exploring_towers(self, towerColorA, towerColorB):
        """
        If directive have one color tower to go is a manual explorer workflow.
        If it have two color towers to go is a autonomous explorer towers
        """
        # if not exist towerB color is manual explorer action based in user directives
        if (towerColorB == ""):
            self.nav_map.set_order_list(
                tower_order_list=[towerColorA.capitalize()])
            logging.info('Begin manual exploring towers ...')
            # Scan all initial towers position
            self.nav_map.scan_finding_towers()
            logging.info('Going ' + towerColorA + ' tower')
            self.nav_map.go_color_tower(towerColorA.capitalize())
            logging.info('Explorer arrive at tower...' + towerColorA)
            self._send_event(EventName.ARRIVE_TOWER.value, {
                'speechOut': "Explorer arrive at " + towerColorA + " tower",
                'botPosition': towerColorA + " tower"})
        # Autonomous explorer workflow
        else:
            logging.info('Begin autonomous exploring towers ...')
            self.nav_map.set_order_list(
                tower_order_list=[towerColorA.capitalize(), towerColorB.capitalize()])
            # Scan all initial towers position
            self.nav_map.scan_finding_towers()
            for tower_color in self.nav_map.tower_order_list:
                # Robot go each tower
                logging.info('Going ' + tower_color + ' tower')
                self._send_event(EventName.GOING_TOWER.value, {
                    'speechOut': "Explorer is going to the " + tower_color + " tower"})
                self.nav_map.go_color_tower(tower_color)
                self._send_event(EventName.ARRIVE_TOWER_AUTO.value, {
                    'speechOut': "Explorer arrive " + tower_color + " tower",
                    'botPosition': tower_color + " tower"})
                sleep(10)
                # At arrive tower read all conditions
                self._send_event(EventName.ALLCONDITIONS.value, {
                    'speechOut': "Reading all conditions at " + tower_color + " tower"})
                self._read_conditions(ConditionName.ALL_CONDITIONS.value)
                sleep(20)
                # And return base
                self._send_event(EventName.RETURN_BASE.value, {
                    'speechOut': "Explorer is returning to the base"})
                self._return_base()

    def _send_event(self, name, payload):
        """
        Sends a custom event to trigger a sentry action.
        :param name: the name of the custom event
        :param payload: the sentry JSON payload
        """
        self.send_custom_event('Custom.Mindstorms.Gadget', name, payload)


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
