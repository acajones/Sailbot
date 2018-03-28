#import gps
#import Adafruit_LSM303
import math
#import CompassDefault

# takes in a destination latitude and longitude, and turns boat towards the destination
def main(destLat, destLon):
  #  currHeading = CompassDefault.getBearing()
	currHeading = 50
	newHeading =  getHeading(583838, 583838, 30412, 30450)
	turnBoat(currHeading, newHeading)


def getHeading(lat1, lat2, long1, long2):
    dy = lat2 - lat1 
    dx = math.cos(math.pi/180*lat1)*(long2-long1)
    angle = math.atan2(dy,dx)
    return 180/math.pi*angle

def turnBoat(currHeading, newHeading):
    change = newHeading - currHeading

    if(change < -75):
        change = -75

    elif(change > 75):
        change = 75
    
    print "New Heading Is: "
    print newHeading
    print "\n"
    print "New Rudder Angle Is: "
    print change
    newFrequency = -1.1078 * change + 387

    #moveservo.main(rudder_channel, newFrequency)
    #moveservo.main(rudder_channel, 437) #left 45 deg
    #moveservo.main(rudder_channel, 337) #right 45 deg
    #moveservo.main(rudder_channel, 387) #straight


#Protects main from being run when imported and only run when executed.
#Runs main()
if __name__ == '__main__':
	main()
