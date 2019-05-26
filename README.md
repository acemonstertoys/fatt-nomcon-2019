# fatt-nomcon-2019
Code to control makerspace-auth board items such as LEDs, locks, and motors using Raspbian Stretch with desktop 4.19.42-v7+ SD card

Author: Blaze Sanders Skype: blaze.sanders Twitter: @BlazeDSanders

This Git repo holds code from multiple open source libraries. It's broken down into the following directories ***(PROJECTS, RPi.GPIO-0.5.11, and CompressedLibraryCode)***.

High level system diagram and detailed wiring schematic can be found at:
https://upverter.com/design/blazesandersinc/d5ddd17fdd70924d/

To run the code in PROJECTS directory complete the following steps:

1) Download this FULL git repo onto a Raspberry Pi 3 B+
2) Use sudo raspi-congig Linux terminal command to setup setup Pi for use
2.1) Use DOWN ARROW and ENTER keys to select Options 5 "Interfacing Options"
2.2) Use DOWN ARROW and ENTER ENter to select P2 SSH, P4 SPI, P5 I2C, and P7 1-Wire
2.3) Use ENTER key to select "<yes>" to enable all four features in step 2.2 above.
2.4) Repeat steps 2.1 to 2.3 for all four features in step 2.2 above.
2.5) Use RIGHT ARROW and ENTER keys to select "<finish>"
3) Use "cd fatt-nomcon-2019" command to navigate to the highest level directory
4) Use "python install.py" command to auto install on the necessary libraries
5) Use "cd PROJECTS/LockBox" command to navigate to 1 of the 3 projects
6) Finally run the command "python3 Driver.py" to start any project software running
7) Open ANY web browser and type http://localhost:8000 into URL box (Google Chrome tested)

NOTE: Use "python3" and NOT "python", in step 5 or you will get run time errors!!!

Note: If not running this code on a Pi3+ change the CONFIG string on line #10 of install.py

***
RPi.GPIO-0.5.11:

https://pypi.org/project/RPi.GPIO/0.5.11/

We will be updating to 0.6.5 https://pypi.org/project/RPi.GPIO/0.6.5/ with further test

***
CompressedLibraryCode:

All external library source code downloaded from author with ZERO changes

***
