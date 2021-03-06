import sys 
sys.path.append('/usr/local/lib/python2.7/site-packages')

# import the necessary packages
from collections import deque
from array import array
from numpy import *
import subprocess
import argparse
import imutils
import cv2
import time
import math
import moveservo
import threading
#import bt_withMain
import gpsdshm
import CompassDefault
import goCoord

gpsd_shm = gpsdshm.Shm()
dirBuoy = "none"
rudder_channel = 3
exitapp = False
x_orig = 0
y_orig = 0

# records coordinates of boat and direction of buoy
# from the boat
coordsList = [
]
endCoords = [] # coordinates of the end of each vector
directionsList = []
iteration = 0

def main():
	stay(90)
	iteration = 0
	thread1 = threading.Thread(target=ballTrack)
	thread1.start()
	while True:
		global dirBuoy
		time.sleep(1)
		print "Direction: ",dirBuoy
		# used to get majority direction in a given time
		left = 0
		straight = 0
		right = 0
		
		#Converts lat and long degrees to meters from equator and prime meridian respectively
		#lat=gpsd_shm.fix.latitude*111*1000 #Latitude in meters from equator
		#lon=gpsd_shm.fix.longitude*Math.cos(gpsd_shm.fix.latitude*3.14/180)*111*1000
		lat = 100.0
		lon = 150.0

		# if the buoy is seen record the boats position
		if dirBuoy !=  'none':
			#coordsList.append(lat)
			#coordsList.append(lon)
			iteration = iteration + 1

			# then record the direction that the buoy is from the boat
			if dirBuoy == 1:
				directionsList.append(CompassDefault.getBearing() - 75)
				
			elif dirBuoy == 2:
				directionsList.append(CompassDefault.getBearing() - 56)	

			elif dirBuoy == 3:
				directionsList.append(CompassDefault.getBearing() - 37)

			elif dirBuoy == 4:
				directionsList.append(CompassDefault.getBearing() - 19)

			elif dirBuoy == 5:
				directionsList.append(CompassDefault.getBearing())

			elif dirBuoy == 6:
				directionsList.append(CompassDefault.getBearing() + 19)

			elif dirBuoy == 7:
				directionsList.append(CompassDefault.getBearing() + 38)

			elif dirBuoy == 8:
				directionsList.append(CompassDefault.getBearing() + 56)

			elif dirBuoy == 9:
				directionsList.append(CompassDefault.getBearing() + 75)
			
			print 'Iteration: ',iteration
			makeVector(iteration)

			# once at least 2 vectors have been made, find the intersection
			if iteration > 1:
				# gets all endpoints from lists and calls seg_intersect with those points
				#print coordsList
				#print endCoords
				a1 = array([ coordsList[0], coordsList[1] ])
				a2 = array([ endCoords[0], endCoords[1] ])
				b1 = array([ coordsList[2], coordsList[3] ])
				b2 = array([ endCoords[2], endCoords[3] ])
				print 'Intersection at: ',seg_intersect(a1,a2,b1,b2)

			leaveCurCoord(lat, lon)

		else:
			# search for buoy
			findBuoy();

# http://stackoverflow.com/questions/3252194/numpy-and-line-intersections
# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    print num, denom, db, b1
    return (num / float(denom))*db + b1

# helper method for seg_intersect
def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# turns rudder 45 degrees left or right to turn
# or moves rudder to center to go straight
def turnBoat(dir):
	if dir == 'left':
		#moveservo.main(rudder_channel, 437)
		print 'rudder left'

	if dir == 'right':
		#moveservo.main(rudder_channel, 337)
		print 'rudder right'

	if dir == 'straight':
		#moveservo.main(rudder_channel, 387)
		print 'rudder straight'

# gets lat and long points 100 meters away in a specified direction for the current iteration
def makeVector(iteration):
	lat = coordsList[iteration-1] + math.cos(directionsList[iteration-1]*3.14/180) * 100
	lon = coordsList[iteration] + math.sin(directionsList[iteration-1]*3.14/180) * 100
	endCoords.append(lat)
	endCoords.append(lon)

# leaves current area to get more data (coordinates and directions)
# for the buoy location
def leaveCurCoord(lat, lon):
	turnBoat('right')
	time.sleep(5)
	turnBoat('straight')

	newLat = lat*111*1000 #Latitude in meters from equator
	#newLon = lon*Math.cos(gpsd_shm.fix.latitude*3.14/180)*111*1000
	newLon = lon + 100

	while abs(newLat - lat) < 4 and abs(newLon - lon) < 4:
		#newLat = gpsd_shm.fix.latitude*111*1000
		#newLon = gpsd_shm.fix.longitude*Math.cos(gpsd_shm.fix.latitude*3.14/180)*111*1000
		newLat = 1
		newLon = 1



# when buoy is not in view, search area for buoy
def findBuoy():
	found = False

	while not found:
		print("searching")
		found = True

# calculates how far the boat is from its origin and sends warning if distance is >= max
def stay(max):
    x_coord = gpsd_shm.fix.latitude
    y_coord = gpsd_shm.fix.longitude
    print x_coord
    distance = ((x_coord - x_orig)**2 + (y_coord - y_orig)**2)**0.5
    if distance >= max:
        print "turn around!"
    else:
        print "all good"
        
def search():
    t = 0

    while(not_found && all_good)
        x_coord = x_orig + t*math.cos(t)
        y_coord = y_orig + t*math.sin(t)
        //sail to (x_coord, y_coord)
        t++

# tracks ball shaped object in recorded video
def ballTrack():
	while not exitapp:
		# take video with pi camera
		subprocess.call("/home/pi/camera/video.sh", shell=True)

		# construct the argument parse and parse the arguments
		ap = argparse.ArgumentParser()
		ap.add_argument("-v", "--video", default="/home/pi/camera/videoMP4.mp4",
			help="path to the (optional) video file")
		ap.add_argument("-b", "--buffer", type=int, default=64,
			help="max buffer size")
		args = vars(ap.parse_args())
		print args

		# define the lower and upper boundaries of the "green"
		# ball in the HSV color space, then initialize the
		# list of tracked points
		redLower = (169, 100, 100)
		redUpper = (189, 255, 255)
		pts = deque(maxlen=args["buffer"])

		# if a video path was not supplied, grab the reference
		# to the webcam
		if not args.get("video", False):
			camera = cv2.VideoCapture(0)

		# otherwise, grab a reference to the video file
		else:
			camera = cv2.VideoCapture(args["video"])

		# keep looping
		while True:
			# executes bash script to take an image and save
			#subprocess.call("/home/pi/camera/camera.sh", shell=True)

			#time.sleep(2)

			#camera = cv2.VideoCapture("/home/pi/camera/image.jpg")

			# grab the current frame
			(grabbed, frame) = camera.read()

			# if we are viewing a video and we did not grab a frame,
			# then we have reached the end of the video
			if args.get("video") and not grabbed:
				print("breaking")
				break

			# resize the frame, blur it, and convert it to the HSV
			# color space
			frame = imutils.resize(frame, width=600)

			blurred = cv2.GaussianBlur(frame, (11, 11), 0)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			# construct a mask for the color "green", then perform
			# a series of dilations and erosions to remove any small
			# blobs left in the mask
			mask = cv2.inRange(hsv, redLower, redUpper)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)

			# find contours in the mask and initialize the current
			# (x, y) center of the ball
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
			center = None
			# only proceed if at least one contour was found
			if len(cnts) > 0:
				# find the largest contour in the mask, then use
				# it to compute the minimum enclosing circle and
				# centroid
				c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

				# only proceed if the radius meets a minimum size
				if radius > 10:
					# draw the circle and centroid on the frame,
					# then update the list of tracked points
					cv2.circle(frame, (int(x), int(y)), int(radius),
						(0, 255, 255), 2)
					cv2.circle(frame, center, 5, (0, 0, 255), -1)
				global dirBuoy
				# frame size is 600, left middle and right are split into 3 zones
				if center[0] < 67:
					dirBuoy = 1
				elif center[0] < 134:
					dirBuoy = 2
				elif center[0] < 201:
					dirBuoy = 3
				elif center[0] < 268:
					dirBuoy = 4
				elif center[0] < 335:
					dirBuoy = 5
				elif center[0] < 402:
					dirBuoy = 6
				elif center[0] < 469:
					dirBuoy = 7
				elif center[0] < 536:
					dirBuoy = 8
				elif center[0] <= 600:
					dirBuoy = 9
				else:
					dirBuoy = "none"
			# update the points queue
			pts.appendleft(center)

			# loop over the set of tracked points
			for i in xrange(1, len(pts)):
				if pts[i - 1] is None or pts[i] is None:
					continue

				# otherwise, compute the thickness of the line and
				# draw the connecting lines
				thickness = int(sqrt(args["buffer"] / float(i + 1)) * 2.5)
				cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

			# show the frame to our screen
			#cv2.imshow("Frame", frame)
			cv2.imwrite("frame.jpg",frame)
			key = cv2.waitKey(1) & 0xFF

			# if the 'q' key is pressed, stop the loop
			if key == ord("q"):
				break

		# cleanup the camera and close any open windows
		camera.release()
		cv2.destroyAllWindows()


#Protects main from being run when imported and only run when executed.
#Runs main()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        raise
