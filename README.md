# fatt-nomcon-2019
Code to control makerspace-auth board items such as LEDs, locks, and motors using Raspbian Stretch with desktop 4.19.42-v7+ SD card

Author: Blaze Sanders Skype: blaze.sanders Twitter: @BlazeDSanders

This Git repo holds code from multiple open source libraries. It's broken down into the following directories ***(PROJECTS, RPi.GPIO-0.5.11, and CompressedLibraryCode)***.

High level system diagram and detailed wiring schematic can be found at:
https://upverter.com/design/blazesandersinc/d5ddd17fdd70924d/

To run the code in PROJECTS directory complete the following steps:

1) Download this FULL git repo onto a Raspberry Pi 3 B+
2) Use "cd fatt-nomcon-2019" Linux terminal command to navigate to the highest level directory
3) Use "python install.py" command to auto install on the necessary libraries
4) Use "cd PROJECTS/LockBox" command to navigate to 1 of the 3 projects
5) Finally run the command "python3 Driver.py" to start any project software running
6) Open ANY web browser and type http://localhost:8000 into URL box (Google Chrome tested)

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
