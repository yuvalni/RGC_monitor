from time import sleep

import serial
import logging
import random

class MockUp():
    def __init__(self):
        print("keithley connected")
    

    def TemperatureA(self):
        return 41 + random.random()

    def TemperatureB(self):
        return 3.2 + random.random()
    

class lakeshore():
    def __init__(self, port='COM6', timeout=1): #rate in seconds
        self.logger = logging.getLogger('lakeshore')
        self.port = port
        self.temperatureA = -999
        self.temperatureB = -999
        self.timeout = timeout
        self.connected = False
        
        try:
            self.ser = serial.Serial(self.port, timeout=self.timeout, stopbits=serial.STOPBITS_TWO)
            self.logger.info('Lakeshore is connectd.')
            self.connected = True
        except:
            self.connected = False
            self.logger.warning('serial is unable to connect.')

        
    
    
    def close(self):
        if self.ser.is_open:
            self.ser.close()
            self.connected = False
        else:
            self.logger.warning('serial is already closed.')

    def read_TemperatureA(self):
        if not self.connected:
            return False
        self.ser.write(b'\r\n')
        sleep(30 / 1000)
        temp = str(self.ser.readline(), 'utf-8')
        self.temperatureA = float(temp)
        return self.temperatureA


    def read_TemperatureB(self):
        if not self.connected:
            return False
        self.ser.write(b'\r\n')
        sleep(30 / 1000)
        temp = str(self.ser.readline(), 'utf-8')
        self.temperatureB = float(temp)
        return self.temperatureB