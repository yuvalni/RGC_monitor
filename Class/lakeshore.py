from time import sleep
import serial

import random

class MockUp():
    def __init__(self):
        print("keithley connected")
    

    def TemperatureA(self):
        return 41 + random.random()

    def TemperatureB(self):
        return 3.2 + random.random()