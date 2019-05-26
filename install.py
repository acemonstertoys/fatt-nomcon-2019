#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Ace Monster Toys"
__status__ =  "Development"
__date__ =    "Late Updated: 2019-05-26"
__doc__ =     "Instsall script to setup run and dev enviroment"

CONFIG = "Pi3B+" # or "UnbuntuOnWindows" of "UbuntuMate" or "Alpine"

# Allow BASH command to be run inside Python3 code like this file
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_call

if __name__ == "__main__":
	check_call("clear",shell=True)  # Clear terminal

	# Check and update your system
	check_call("sudo apt update", shell=True)
	check_call("sudo apt upgrade", shell=True)

	# Allow other computers to SSH into Pi (SSH not always installed on Pi distros)
	check_call("sudo apt install openssh-server", shell=True)
	check_call("sudo apt install sshguard", shell=True)

	# Flask requires Python 3 to work
	check_call("sudo apt install python3-pip", shell=True)

	# Flask is the GUI frontend to that runs in parallel with python backend controling pumps
	# Remember to run flask with "python3" NOT "python" command, or you will get weird errors :)
	# https://aryaboudaie.com/python/technical/educational/web/flask/2018/10/17/flask.html
	check_call("pip3 install flask", shell=True)

	# Low level control on GPIO pins to drive Servo, Motor, Relays, LED, etc
	# Python 3 install of GPIO and servo to match Flask
	# https://gpiozero.readthedocs.io/en/stable/installing.html
	if(CONFIG == "Pi3B+"):
		check_call("sudo apt install python3-gpiozero", shell=True)
	elif(CONFIG == "UbuntuOnWindows"):
		check_call("sudo pip install gpiozero", shell=True)
	elif(CONFIG == "UbuntuMate"):
		print("TODO")
		#TODO TEST check_call("sudo pip install gpiozero", shell=True)
	elif(CONFIG == "Alpine"):
		print("TODO")
		#TODO TEST check_call("sudo apt install python3-gpiozero", shell=True)
	else:
		print("INVALID CONFIG SELECTED")

	#IF GPIO ZERO FAILS AND IS NOT POWERFUL ENOUGH
	#pip install RPi.GPIO
	#sudo pip3 install adafruit-circuitpython-motorkit
