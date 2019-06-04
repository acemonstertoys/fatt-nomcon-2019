
#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Ace Monster Toys"
__status__ =  "Development"
__date__ =    "Late Updated: 2019-06-01"
__doc__ =     "Main control code for Minty Box project"

# Modular plug and play control of motors, servos, and relays
import Actuator

# Custom code to get JSON data from web API and check against white list
#import JSON

# Allow control of output devices such as Motors, Servos, LEDs, and Relays
from gpiozero import Motor, Servo, LED, Energenie, OutputDevice

# Allow control of input devices such as Buttons
from gpiozero import Button

# Useful for controlling devices based on date and time
from gpiozero import TimeOfDay  # Used to get date and time down to the minute
import datetime			# Used to get current time down to millisecond
import time			# Used to pause code


# Useful CONSTANTS to allow quick update of software, when hardware changes
RELAY_RL1_MAKER_SPACE_AUTH_BOARD_J12 = 6	# Physical Pin 31 / BCM-6
PIN_PWR_3V3 = 23			 	# Physical Pin 16 / BCM-23
PWR_12V = "J12-1"
GND = "BOARD6"
PIN_D0 = 4					# Physical Pin 7 / BCM-4
PIN_D1 = 27					# Physical Pin 13 / BCM-27

if __name__  == "__main__":

	pinPower = OutputDevice(PIN_PWR_3V3) 	# BCM-23
	lock = OutputDevice(RELAY_RL1_MAKER_SPACE_AUTH_BOARD_J12) # BCM-6

	RFID_Data0 =  OutputDevice(PIN_D0) 	# Physical Pin 7 / BCM-4
	RFID_Data1 = OutputDevice(PIN_D1) 	# Physical Pin 13 / BCM-27

	while True:
		print("Start Minty Box Main Function:")
		# Power LOW side of HiLetGo 5 to 3.3V logic level converter
		pinPower.on()
		print("3.3V pin power on:")

		time.sleep(3)	# Pause 3 seconds before next test


		#JSON.getJSON()

		print("Unlock:")
		lock.on() 	# Unlock
		time.sleep(1.5) # Pause 1.5 seconds = 1500 milliseconds
		lock.off()	# Lock
		print("Locked:")

		time.sleep(3)	# Pause 3 seconds before next test

		print("Turn RFID pins HIGH")
		RFID_Data0.on()
		RFID_Data1.on()
		time.sleep(5)	# Pause 3 seconds before next test
		print("Turn RFID pins LOW")
		RFID_Data0.off()
		RFID_Data1.off()

		print("End Minty Box Main Function")
