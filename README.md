# pi-nixie-clock
Raspberry Pi powered Nixie clock project

# Hardware
* Uses a Raspberry Pi Zero W 
* Pi Breadboard GPIO breakout board. I soldered this into my stripboard to make getting at the pins more convenient.  
* 6x K155ID1 driver IC, along with some IN-12B Nixie tubes. I used a 22k resistor on each anode. Subesquent research suggests 16k is ideal. 
* INS-1 lamps for time seperators. Could do it with fewer ICs if multiplexing.
* High-current transistors for the INS-1 dot lamps. I used 2x MPSA42 with each driving 2 dots; worked fine with 222k resistance. If I did it again, I'd have gone up to 250k as they're noticably brighter than the Nixies. 
* Advice: Well worth getting the proper IN-12B tube holders.
* 170V step-up transformer needed (draws very little current, so a cheap one will do
* 12V DC transformer for the wall
* Buck transformer to give 5V to the Pi.
* Can be soldered onto a single stripboard sheet, if you're patient. It's what I did. 
* Laser-cut a nice box to keep it all in. 

# Software
* Use the dTest.py to ensure that everything is working. It'll pulse the dots on and off, and show all digits.
* Set up as a cron job (@reboot	  /home/pi/pi-nixie-clock/nixie.py) on startup so you can plug and unplug it.
* Relies on the Pi for timekeeping (uses network time), so needs WiFi connection and locale set up correctly.

# Updates
* 9/6/19 - Added some scrolling animations for when the date is shown, and disguised the cathode protection as an animation. Also added SolidWorks model, DXFs and a TechSoft 2D cutting sheet for the housing (assuming you build onto a single sheet of stripboard like I did). 