# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
# import logging
# logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address=0x70)

# Configure min and max servo pulse lengths
servo_min = 225 #225  # Min pulse length out of 4096
servo_max = 575 #575  # Max pulse length out of 4096

servo_one_pos = 387
servo_two_pos = 387
servo_three_pos = 400

# Rudder servo has minimum range of 225 and max range of 575
# to move it make sure address=0x70
# rudder is on channel 3 = 400 = neutral
# main sail is on channel 1 = 368 = neutral
# secondary sale is on channel 2 = 331 = neutral

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def main(ch, sig):
    # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)
    pwm.set_pwm(ch, 0, sig)
    return

if __name__ == "__main__": main(ch, dir)

