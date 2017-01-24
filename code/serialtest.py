import time
import serial

port = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=3.0)

while True:
    name = raw_input("Write something to the computer")
    port.write(name)
#    port.write("I heart emoji this")
    rcv = port.read(10)
    print "\r\nYou sent:" + repr(rcv)
