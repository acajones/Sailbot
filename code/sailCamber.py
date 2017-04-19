#Sail camber determination

import math
import analogTest
import moveservo
import time


# channels for servos
mainsail_channel = 4
aftsail_channel = 5




# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# 10k trim pot connected to adc #0
potentiometer_adc = 0;

# calculates main sail angle depending on angle of wind direction sensor
def mainSailAngle():
	windAngle = analogTest.readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	print("Wind Ange: "+windAngle)

	# converts raw wind sensor output to radians
	rads = ((((windAngle)/920.0-50)*(2*math.pi))-((2*math.pi)/23))

	# equation abs(-180*sin(radians)+150) calulates main sail angle from wind angle radians
	mainSail = abs(-180*math.sin(rads) + 150)

	moveservo.main(mainsail_channel, int(mainSail))
	print(mainSail)


# first move main sail to neutral position
moveservo.main(mainsail_channel, 400)
time.sleep(3)

while True:
	mainSailAngle()
	time.sleep(0.5)
