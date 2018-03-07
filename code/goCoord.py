#import gps
#import Adafruit_LSM303
import math

def main():
    currHeading = 0
    newHeading =  getHeading(583838, 583838, 30412, 30450)
    turnBoat(heading)


def getHeading(lat1, lat2, long1, long2):
    dy = lat2 - lat1 
    dx = math.cos(math.pi/180*lat1)*(long2-long1)
    angle = math.atan2(dy,dx)
    return 180/math.pi*angle

def turnBoat(currHeading, newheading):
    change = newHeading - currHeading

    if(change < -75):
        change = -75

    elif(change > 75):
        change = 75
    
    newFrequency = -1.1078 * change + 387

    moveservo.main(rudder_channel, newFrequency)
    #moveservo.main(rudder_channel, 437) #left 45 deg
    #moveservo.main(rudder_channel, 337) #right 45 deg
    #moveservo.main(rudder_channel, 387) #straight


#Protects main from being run when imported and only run when executed.
#Runs main()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        raise
