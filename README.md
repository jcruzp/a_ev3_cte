# a_ev3_csf_bot

Autonomous EV3 Color Station Finder Bot 

Autonomous Color Station EV3 is a bot that scan a field searching three color stations, red, blue and yellow and go to each station based in Alexa directives. 

At arrive each station bot check the right color, temperature, pressure, GPS position and some other variables at his location.

Output_A = Color Arm Medium Motor - Yellow Leds
Output_B = Scan Tower Large Motor - Red Leds
Output_C = Car Engine Large Motor - Orange Leds
Output_D = Steering Wheel Medium Motor - Green Leds

Input_1 = Color
Input_2 = Temperature
Input_3 = Gyroscope
Input_4 = Pixy2   (Ultrasonic)


Declaratives

Control payload: {'type': 'exploring_towers', 'towerColorA': 'blue'}
Control payload: {'type': 'exploring_towers', 'towerColorA': 'red'}
Control payload: {'botposition': 'red tower', 'condition': 'GPS position', 'type': 'read_conditions'}
Control payload: {'botposition': 'red tower', 'condition': 'ambient temperature', 'type': 'read_conditions'}
Control payload: {'botposition': 'red tower', 'condition': 'relative humidity', 'type': 'read_conditions'}
Control payload: {'type': 'return_base'}
Control payload: {'botposition': 'red tower', 'type': 'verify_color'}

Session Values

botPosition = base, red tower, blue tower


Events

    ARRIVE_TOWER = "at_tower"
    ARRIVE_BASE = "at_base" 
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    COLOR = "color"
    GPS = "gps"

