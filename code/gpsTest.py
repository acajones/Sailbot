import serial
import threading
import time
import datetime


port = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=0.5)

def main():
    data = port.readline().decode()
    print data
