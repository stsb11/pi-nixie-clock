# Nixie Digit tester
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # I.e. the 5V pin in the top-left corner is referred to as 2.

# Wiring below, to K155ID1 IC ABCD inputs (A is LSB, D is MSB).
# Each sub-list goes from MSB to LSB (D to A). 

# Top-left most (hrs tens)
# A: GPIO11 B:6 C:13 D:5
lamp1 = [3, 17, 4, 2]

# Top-middle (hrs units)
# A: GPIO27  B:10 C:9 D: 22
lamp2 = [22, 9, 10, 27]

# Top-right most (mins tens)
# A: GPIO2 B:4 C:17 D: 3
lamp3 = [5, 13, 6, 11]

# Bottom-left most (minutes units)
# A: GPIO12 B:20 C:21 D: 16
lamp4 = [16, 21, 20, 12]

# Bottom-middle (seconds tens)
# A: GPIO24 B: 8  C: 7  D: 25
lamp5 = [25, 7, 8, 24]

# Bottom-right IC (nearest female connector to Pi; seconds units)
# A: GPIO18 B: 14 C: 15 D: GPIO23
lamp6 = [23, 15, 14, 18]

# Pairs of dots
bDots = 26
tDots = 19
GPIO.setup(bDots, GPIO.OUT)
GPIO.setup(tDots, GPIO.OUT)
# object = GPIO.PWM(pin, frequency)
# object.start(50)
# object.stop()
pbDots = GPIO.PWM(bDots, 100)
lamps = [lamp1, lamp2, lamp3, lamp4, lamp5, lamp6]
    
for lamp in lamps:
    for pin in lamp:
        GPIO.setup(pin, GPIO.OUT)

# ****************************
# Functions start here
# ********************

def lightUp(lamp, numToShow):
    global lamps
    # Pass in which Nixie tube (1-6) and the digit to show (0 to 9)
    # Showing a digit where the value is >9 turns it off, when using the K155ID1 IC.
    lamp = lamp - 1
    binNum = str(bin(numToShow))[2:]   # binNum will be something like '10'

    while len(binNum) < 4:  # Add leading zeroes to get it to 4 bits.
        binNum = '0' + binNum 
        
    GPIO.output(lamps[lamp][0], int(binNum[0]))
    GPIO.output(lamps[lamp][1], int(binNum[1]))
    GPIO.output(lamps[lamp][2], int(binNum[2]))
    GPIO.output(lamps[lamp][3], int(binNum[3]))    
    # print("Lamp " + str(lamp + 1) + " showing " + str(numToShow))


# *********************************
# Main loop starts here
# ***************

duty = 0
changeby = 1

while True:
    duty = duty + changeby

    if duty > 50:
        changeby = -1
        duty = 50
    elif duty<0:
        changeby = 1
        duty = 0

    pbDots.start(duty)
    lightUp(2, duty % 10)
    lightUp(1, duty // 10)
    time.sleep(0.1)




while True:
    dots = False

    for x in range(10):
        for y in range(1, 7):
            lightUp(y, x)
            print('Showing ' + str(x) + ' on all Nixie tube')
        
        dots = not dots
        GPIO.output(tDots, dots)
        GPIO.output(bDots, dots)
	time.sleep(0.2)
