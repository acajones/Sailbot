#Sail camber determination

import math
import analogTest
import moveservo



mainsail_channel = 4
aftsail_channel = 5
rudder_channel = 3

while true:





def mainSailAngle():
	windAngle = moveservo.readadc()

	#calculates main saile angle from the wind direction
	mainAngle = 180*math.sin(windAngle) + 150
	moveservo.main(mainsail_channel, mainAngle)