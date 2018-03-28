# Simple demo of of the LSM303 accelerometer & magnetometer library.

# Will print the accelerometer & magnetometer X, Y, Z axis values every half

# second.

# Author: Tony DiCola

# License: Public Domain

import time

# Import the LSM303 module.
import math
import Adafruit_LSM303
# Alternatively you can specify the I2C bus with a bus parameter:

# lsm303 = Adafruit_LSM303.LSM303(busum=2)

# Create a LSM303 instance.

lsm303 = Adafruit_LSM303.LSM303()
	
def main():
	while True:
		  # Read the X, Y, Z axis acceleration values and print them.

		  accel, mag = lsm303.read()

		  # Grab the X, Y, Z components from the reading and print them out.

		  accel_x, accel_y, accel_z = accel

		  mag_x, mag_z, mag_y = mag

		  heading = (math.atan2(mag_y,mag_x) * 180) / math.pi

		  if heading < 0:

		      heading = 360 + heading

		  print heading

		  # Wait half a second and repeat.

		  time.sleep(0.5)
		  
def getBearing():
		  # Read the X, Y, Z axis acceleration values and print them.

	accel, mag = lsm303.read()

		  # Grab the X, Y, Z components from the reading and print them out.

	accel_x, accel_y, accel_z = accel

	mag_x, mag_z, mag_y = mag

	heading = (math.atan2(mag_y,mag_x) * 180) / math.pi

	if heading < 0:

		heading = 360 + heading
		      
	return heading
	


#Runs main()
if __name__ == "__main__": main()
