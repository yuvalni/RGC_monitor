#import pyserial
from time import sleep
import serial
import logging
import random

class MockUp():
    def __init__(self):
        print("compressor connected")


    def read_pressure(self):
        sleep(0.3)
        return 200 + random.random()*10

    def read_water_temperature(self):
        sleep(0.3)
        return (17.5 + random.random(),18 + random.random(),16 + random.random())


class Compressor():
    def __init__(self, port='COM9', timeout=1): #rate in seconds
        self.logger = logging.getLogger('compressor')
        self.port = port
        self.pressure = -999
        self.timeout = timeout
        self.connected = False

        try:
            self.ser = serial.Serial(self.port, timeout=self.timeout,baudrate=9600)
            print('compressor is connectd.')
            self.connected = True
        except:
            self.connected = False
            print('serial is unable to connect.')

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
        self.ser.write(b'$PRA95F7\r')
        sleep(30 / 1000)
        string_pressure = str(self.ser.readline(), 'utf-8')

        if(string_pressure.split(',')[0] == "$PRA"):
            self.pressure = float(float(string_pressure.split(',')[1]))

            #self.ser.write(b'$PR171F6\r')
            #sleep(30 / 1000)
            #string_pressure = str(self.ser.readline(), 'utf-8')

            return self.pressure
        else:
            print('something is wrong.')
            return -999
        # print(string) #properly parse the answer
        # return pressure


    def read_water_temperature(self):
        if not self.connected:
            return False
        self.ser.write(b'$TEAA4B9\r')
        sleep(30 / 1000)
        string_Temp = str(self.ser.readline(), 'utf-8')

        if(string_Temp.split(',')[0] == "$TEA"):
            self.He_Capsule = float(string_Temp.split(',')[1])
            self.WaterTempOut = float(string_Temp.split(',')[2])
            self.WaterTempIn = float(string_Temp.split(',')[3])
            return (self.He_Capsule,self.WaterTempOut,self.WaterTempIn)
        else:
            print('something is wrong')
            return (-999,-999,-999)


    def check_status(self):
        if not self.connected:
            return False
        self.ser.write(b'$STA3504\r')
        sleep(30 / 1000)
        string_Temp = str(self.ser.readline(), 'utf-8')

        if(string_Temp.split(',')[0] == "$STA"):
            print(string_Temp.split(',')[1])
            return True
        else:
            print('something is wrong.')
            return False

    def Turn_on(self):
        if not self.connected:
            return False
        self.ser.write(b'$ON177CF\r')
        sleep(30 / 1000)
        string_Temp = str(self.ser.readline(), 'utf-8')
        if (string_Temp.split(',')[0] == "$ON1"):
            return True
        else:
            print("somthing is worng.")
            return False

    def Turn_off(self):
        if not self.connected:
            return False
        self.ser.write(b'$OFF9188\r')
        sleep(30 / 1000)
        string_Temp = str(self.ser.readline(), 'utf-8')
        if (string_Temp.split(',')[0] == "$OFF"):
            return True
        else:
            print("somthing is worng.")
            return False