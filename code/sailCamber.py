#Sail camber determination

import math
import analogTest
import moveservo
import time


# channels for all servos
mainsail_channel = 4
aftsail_channel = 5
rudder_channel = 3




# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# 10k trim pot connected to adc #0
potentiometer_adc = 0;

def mainSailAngle():
	windAngle = analogTest.readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	print(windAngle/920.0)

	rads = ((((windAngle)/920.0)*(2*math.pi))-((2*math.pi)/23))
	print(rads)
	#calculates main saile angle from the wind direction
	mainSail = 180*math.sin(rads) + 150

	moveservo.main(mainsail_channel, int(mainSail))
	print(mainSail)


moveservo.main(mainsail_channel, 400)
print("centered")
time.sleep(5)
while True:
	# first move main sail to neutral position

	mainSailAngle()
	time.sleep(0.5)
