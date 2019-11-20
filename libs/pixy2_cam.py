
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

# class DataCam():
      
#     def __init__(self):
#         self.sig=0
#         self.x=0
#         self.y=0
#         self.w=0
#         self.h=0   

class Pixy2Cam():
    """
    Control Pixy2 cam at top of tower
    """
    
    def __init__(self):
          
        # Set LEGO port for Pixy2 on input port 1
        lego_port = LegoPort(INPUT_4)
        lego_port.mode = 'other-i2c'
        sleep(0.5)
        # Settings for I2C (SMBus(3) for INPUT_4)
        self.lego_bus =  SMBus(6)
        # Make sure the same address is set in Pixy2
        self.address = 0x54 

    def set_leds(self, turn=0):
        data = [174, 193, 22, 2, turn , 0]
        self.lego_bus.write_i2c_block_data(self.address, 0, data)
        block = self.lego_bus.read_i2c_block_data(self.address, 0, 10)  
      
    def find_object(self, signature=1):
        # Data for requesting block
        data = [174, 193, 32, 2, signature, 1]
        # Request block
        self.lego_bus.write_i2c_block_data(self.address, 0, data)
        # Read block
        block = self.lego_bus.read_i2c_block_data(self.address, 0, 20)
        # Extract data
        #data_cam=DataCam()
        #data_cam.sig = block[7]*256 + block[6]
        #data_cam.x = block[9]*256 +  block[8]
        #data_cam.y = block[11]*256 +  block[10]
        #data_cam.w = block[13]*256 +  block[12]
        #data_cam.h = block[15]*256 +  block[14]
        
        data_cam={}
        data_cam['sig'] = block[7]*256 + block[6]
        data_cam['x'] = block[9]*256 +  block[8]
        data_cam['y'] = block[11]*256 +  block[10]
        data_cam['w'] = block[13]*256 +  block[12]
        data_cam['h'] = block[15]*256 +  block[14]
        return data_cam


