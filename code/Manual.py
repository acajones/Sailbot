#Sailbot main program to visualize sensor information and input commands to
#the boat over RF communication
#-------------------------------------
#All imports for the program
import time
import datetime
import signal
import serial
#the below is an import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import moveservo
import gpsInfo
import threading

#-------------------------------------
#All custom classes for the program
#-------------------------------------
#Custom exception for input timeouts
class InputTimedOut(Exception):
    pass
#-------------------------------------

#Globals
info = ""
#SERVO 1
#LOW: 200 MED: 387 HIGH: 575
#SERVO 4
#LOW: 200 MED: 387 HIGH: 575
#SERVO 3
#LOW: 225 MED: 400 HIGH: 575
degreeInfo = "387|387|400|"
gpsData = "|0.0|0.0"
command = ""

#The main function which runs continuously, prints out information from
#displaySensorInfo() and polls user for one of the following commands:

#Command List:
#    1,2,3 moves the rudder left, nuetral, and right respectively
#    4,5,6 moves the aft sail left, nuetral, and right respectively
#    7,8,9 moves the main sail left, nuetral, and right respectively
 
def main():
    global command 
    servo_one_sig = 387
    servo_two_sig = 387
    servo_three_sig = 400
    threading1 = threading.Thread(target=getCommand)
    threading1.start()
    mainsail_channel = 4
    aftsail_channel = 5
    rudder_channel = 3
    move_by = 30
#    moveservo.main(mainsail_channel, 387)
#    moveservo.main(aftsail_channel, 387)
#    moveservo.main(rudder_channel, 400)
    while True:
        if not command:
            print "main: empty"
        else:
            print "main: " + command
        #Commands to move servos
	    if command == "1" and servo_three_sig > 225:
                servo_three_sig -= move_by
		moveservo.main(mainsail_channel, servo_three_sig)
        if command == "2" and servo_three_sig > 225:
                servo_three_sig = 400
        moveservo.main(mainsail_channel, servo_three_sig)
        if command == "3" and servo_three_sig < 575:
                servo_three_sig += move_by
		moveservo.main(mainsail_channel, servo_three_sig)
        if command == "4" and servo_two_sig > 200:
                servo_two_sig -= move_by
		moveservo.main(aftsail_channel, servo_two_sig)
        if command == "5" and servo_three_sig > 225:
                servo_three_sig = 387
                moveservo.main(aftsail_channel, servo_three_sig)
        if command == "6" and servo_two_sig < 575:
                servo_two_sig += move_by
		moveservo.main(aftsail_channel, servo_two_sig)
        if command == "7" and servo_one_sig > 200:
                servo_one_sig -= move_by
		moveservo.main(rudder_channel, servo_one_sig)
        if command == "8" and servo_three_sig > 225:
                servo_three_sig = 387
        moveservo.main(rudder_channel, servo_three_sig)
        if command == "9" and servo_one_sig < 575:
                servo_one_sig += move_by
        moveservo.main(rudder_channel, servo_one_sig)
        rfSend("Connected")
        displaySensorInfo()
 
#Function to continuously polls the rf for a user command
#args: 
#    p = port for for communication
def getCommand():
    global command
    while True:
        time.sleep(0.5)
        command = raw_input("Give command: ")
        print "thread command: " + command

#Function to retrieve data from gps
def gps():
    try:
        gpsData = gpsInfo.main()
    except:
        print "gps signal error"
    return gpsData
    
#Function to display all sensor information on the command console
def displaySensorInfo():
    info = datetime.datetime.now().strftime("%Y-%m-%d") + "|" + datetime.datetime.now().strftime("%H:%M:%S") + "|"
    #Software SPI configuration:
    CLK  = 18
    MISO = 23
    MOSI = 24
    CS   = 25
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

    #Leave this commented out unless you want to use the hardware SPI configuration
    #over the sotware one above

    #Hardware SPI configuration:
    #SPI_PORT   = 0
    #SPI_DEVICE = 0
    #mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#    rfSend('Reading MCP3008 values, press Ctrl-C to quit...')
    
    #Print nice channel column headers.
#    rfSend('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
#    rfSend('-' * 57)

    # Read all the ADC channel values in a list.
#    values = [0]*8
#    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
#        values[i] = mcp.read_adc(i)
    #Print the ADC values.
#    info += ('|{0:>4}|{1:>4}|{2:>4}|{3:>4}|{4:>4}|{5:>4}|{6:>4}|{7:>4}|'.format(*values))
    info += degreeInfo + str(mcp.read_adc(3)) + "|" + str(mcp.read_adc(5))   
    info += gpsData + "$"
#    info += gpsData
    rfSend(info) 

#Function to send a string over the rf
def rfSend(str):
    port = serial.Serial("/dev/ttyS0", baudrate=57600, timeout = 0.5)
    time.sleep(0.25)
    port.write(str + '\r' + '\n')
    print str

#Protects main from being run when imported and only run when executed.
#Runs main()
if __name__ == "__main__": main()
