# a_ev3_cte

Autonomous EV3 Color Tower Explorer 

Autonomous EV3 Color Tower Explorer is a lego robot that scan a field searching two color towers, red and  blue and go to each tower based in Alexa directives. 

At arrive each tower it check the right color, temperature, humidity, GPS position and some other variables at his location.

Output_A = Color Arm Medium Motor - Yellow Leds
Output_B = Scan Tower Large Motor - Red Leds
Output_C = Car Engine Large Motor - Orange Leds
Output_D = Steering Wheel Medium Motor - Green Leds

Input_1 = Color
Input_2 = Temperature
Input_3 = Gyroscope
Input_4 = Pixy2   (Ultrasonic)


Declaratives

Control payload: {'botposition': 'red tower', 'type': 'exploring_towers', 'towerColorA': 'blue'}
Control payload: {'botposition': 'red tower', 'type': 'exploring_towers', 'towerColorA': 'red'}
Control payload: {'botposition': 'red tower', 'condition': 'GPS position','type': 'read_conditions'}
Control payload: {'botposition': 'red tower', 'condition': 'ambient temperature','type': 'read_conditions'}
Control payload: {'botposition': 'red tower', 'condition': 'relative humidity','type': 'read_conditions'}
Control payload: {'botposition': 'red tower', 'condition': 'all conditions','type': 'read_conditions'}
Control payload: {'botposition': 'red tower', 'type': 'return_base'}
Control payload: {'botposition': 'red tower', 'type': 'verify_color'}

Session Values

botPosition = base, red tower, blue tower


Events

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

