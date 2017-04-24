import moveservo
import threading
import bt_withMain
import time

thread1 = threading.Thread(target=bt_withMain.main())
global dirBuoy;

rudder_channel = 3

# records coordinates of boat and direction of buoy
# from the boat
coordsList = []
directionsList = []

while True:
	print("start")
	# used to get majority direction in a given time
	left = 0
	straight = 0
	right = 0

	i = 0
	while i < 10:
		if dirBuoy == 'left':
			turnBoat('left')

		if dirBuoy == 'straight':
			coordsList.append(gps().coordinates())
			directionsList.append(gps().direction())
			leaveCurCoord()


		if dirbuoy == 'right':
			turnBoat('right')
			

# turns rudder 45 degrees left or right to turn
# or moves rudder to center to go straight
def turnBoat(dir):
	if dir == 'left':
		moveservo.main(rudder_channel, 437)

	if dir == 'right':
		moveservo.main(rudder_channel, 337)

	if dir == 'straight':
		moveservo.main(rudder_channel, 387)


# leaves current area to get more data (coordinates and directions)
# for the buoy location
def leaveCurCoord():
	turnBoat('right')
	time.sleep(10)
	turnBoat('straight')


#Function to retrieve data from gps
def gps():
    try:
        gpsData = gpsInfo.main()
    except:
        print "gps signal error"
    return gpsData