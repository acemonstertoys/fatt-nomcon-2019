#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Ace Monster Toys"
__status__ =  "Development"
__date__ =    "Late Updated: 2019-05-26"
__doc__ =     "Main control code for LockBox project"

# Modular plug and play control of motors, servos, and relays
import Actuator

RELAY_??_MAKER_SPACE_AUTH_BOARD_V?? = 12

if __name__  == "__main__":
	lockPins = [PWR_12V, GND, 12]
	lock = Actuator("R", lockPins, "X001TEYAM1 Locking", Actuator.CW)

	lock.actuate(1.500) #Unlock for 1500 ms or 1.5 seconds
