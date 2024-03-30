#import pyserial
from time import sleep
import serial
import logging
import random

class MockUp():
    def __init__(self):
        print("compressor connected")
    

    def read_pressure(self):
        return 200 + random.random()*10

    def read_water_temperature(self):
        return 16 + random.random()


class compressor():
    def __init__(self, port='COM6', timeout=1): #rate in seconds
        self.logger = logging.getLogger('compressor')
        self.port = port
        self.pressure = -999
        self.timeout = timeout
        self.connected = False
        
        try:
            self.ser = serial.Serial(self.port, timeout=self.timeout, stopbits=serial.STOPBITS_TWO)
            self.logger.info('compressor is connectd.')
            self.connected = True
        except:
            self.connected = False
            self.logger.warning('serial is unable to connect.')

        self.pressure = -999.0
    
    
    def close(self):
        if self.ser.is_open:
            self.ser.close()
            self.connected = False
        else:
            self.logger.warning('serial is already closed.')

    def read_pressure(self):
        if not self.connected:
            return False
        self.ser.write(b'\r\n')
        sleep(30 / 1000)
        string_pressure = str(self.ser.readline(), 'utf-8')
        self.pressure = float(string_pressure)
        return self.pressure
        # print(string) #properly parse the answer
        # return pressure


    def read_water_temperature(self):
        if not self.connected:
            return False
        self.ser.write(b'\r\n')
        sleep(30 / 1000)
        string_Temp = str(self.ser.readline(), 'utf-8')
        self.WaterTemp = float(string_Temp)
        return self.WaterTemp