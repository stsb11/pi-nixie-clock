# pi-nixie-clock
Raspberry Pi powered Nixie clock project

# Hardware
* Uses a Raspberry Pi Zero W (needs WiFi connection and locale set up correctly to get the time)
* Also uses K155ID1 driver IC, along with some IN-12B Nixie tubes and some nice INS-1 lamps for time seperators.
* Advice: Well worth getting the proper IN-12B tube holders.
* 170V step-up transformer needed (draws very little current, so a cheap one will do
* 12V DC transformer for the wall
* Buck transformer to give 5V to the Pi.
* Can be soldered onto a single stripboard sheet, if you're patient.

# Software
* Use the dTest.py to ensure that everything is working. It'll pulse the dots on and off, and show all digits.
* Set up as a cron job (@reboot	  /home/pi/pi-nixie-clock/nixie.py) on startup so you can plug and unplug it.
* Laser-cut a nice box to keep it all in. 