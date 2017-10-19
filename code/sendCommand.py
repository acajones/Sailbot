import serial
import threading
import time
import datetime

port = serial.Serial("/dev/ttyUSB2", baudrate=57600, timeout=0.5)
command = ""
check = ""

def main():
    global check
    global command
    global port
    print "running main"
#   port = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=0)
#    port = serial.Serial("COM4", baudrate=57600, timeout=0.5)
    threading1 = threading.Thread(target=readPIInput)
    threading1.start()
    threading2 = threading.Thread(target=readUserInput)
    threading2.start()
    while True:
        if command != check:
            sendCommand(command)
            check = ""
            command = ""
            time.sleep(.1)

def readPIInput():
    data = ""
    global port
    while True:
        #data = datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S") + "|" + str(servo1) + "|" + str(servo2) + "|" + str(servo3) + "|" + str(windspeed) + "|" + str(winddirection) + "|" + str(0.0) + "|" + str(0.0) + " $"
       # data = port.readline().decode()
        print data
        target = open("data.txt", 'w')
        target.write(data)
        target.close
        time.sleep(0.5)

def readUserInput():
    global command
    while True:
        command = raw_input("Enter a Command!")
        time.sleep(0.5)

def sendCommand(str):
    global port
    print "sending"
    print "port opened"
   # port = serial.Serial("/dev/ttyUSB1", baudrate=57600, timeout=0.5)
    port.write(str)
    print "sent " + str

if __name__ == "__main__":
    main()
