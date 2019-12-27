
# Jose Cruz - 2019
# email: joseacruzp@gmail.com
# twitter: @joseacruzp
# github:  https://github.com/Jcruzp
# website: https://sites.google.com/view/raeiot

from ev3dev2.display import Display
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.port import LegoPort

from smbus import SMBus
from time import sleep
from enum import IntEnum

class SignatureColor(IntEnum):
    NONE = 0
    RED = 1
    BLUE = 2
    YELLOW = 3

class Pixy2Cam():
    """
    Control Pixy2 cam at top of tower
    """
    
    def __init__(self):
          
        # Set LEGO port for Pixy2 on input port 4
        lego_port = LegoPort(INPUT_4)
        lego_port.mode = 'other-i2c'
        sleep(0.5)
        # Settings for I2C (SMBus(6) for INPUT_4)
        self.lego_bus =  SMBus(6)
        # Pixy2 address
        self.address = 0x54 

    def turn_lamp_on(self):
        data = [174, 193, 22, 2, 1 , 0]
        self.lego_bus.write_i2c_block_data(self.address, 0, data)
        sleep(0.1)
              
    def turn_lamp_off(self):
        data = [174, 193, 22, 2, 0 , 0]
        self.lego_bus.write_i2c_block_data(self.address, 0, data)
        sleep(0.1)
      
    def find_object(self, signature):
        if signature == 3: 
            signature_search = 6
        else:
            signature_search = signature
            
         # Data for requesting block
        data = [174, 193, 32, 2, signature_search, 1]
            
        sig_data_return=0
        while sig_data_return != signature: 
                       
            # Request block
            self.lego_bus.write_i2c_block_data(self.address, 0, data)
            sleep(0.1)
            # Read block
            block = self.lego_bus.read_i2c_block_data(self.address, 0, 20)
            sleep(0.1)
                
            data_cam={}
            data_cam['sig'] = block[7]*256 + block[6]
            data_cam['x'] = block[9]*256 +  block[8]
            data_cam['y'] = block[11]*256 +  block[10]
            data_cam['w'] = block[13]*256 +  block[12]
            data_cam['h'] = block[15]*256 +  block[14]
            sig_data_return=data_cam['sig']
            
        return data_cam

    def object_distance(self, object_width=1):
        """
        Calculate object distance in inches based on camera focal length.
        W know width of object 
        D know distance from camera before take a picture
        P know width in pixeles of object at distance D
        F = (P x D) / W
        D = (W x F) / P
        :param object_width: width in pixeles for object detected by signature
        """
        W = 1 # 1 inche tower width
        D = 12 # 12 inches distance form tower to cam before take a picture
        P = 22 # at 12 inches the 1 inch tower width see with 22 pixeles in cam image
        F = (P * D) / W
        D = (W * F) / object_width # object_width is new P object width
        return D