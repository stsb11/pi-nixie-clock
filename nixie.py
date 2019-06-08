# Nixie GPS-powered clock, v0.1
import datetime, random, time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # I.e. the 5V pin in the top-left corner is referred to as 2.
GPIO.setwarnings(False)

# Wiring below, to K155ID1 IC ABCD inputs (A is LSB, D is MSB).
# Each sub-list goes from MSB to LSB (D to A). 

# Top-left most (hrs tens)
# A: GPIO11 B:6 C:13 D:5
lamp1 = [5, 13, 6, 11]

# Top-middle (hrs units)
# A: GPIO27  B:10 C:9 D: 22
lamp2 = [22, 9, 10, 27]

# Top-right most (mins tens)
# A: GPIO2 B:4 C:17 D: 3
lamp3 = [3, 17, 4, 2]

# Bottom-left most (minutes units)
# A: GPIO12 B:20 C:21 D: 16
lamp4 = [16, 21, 20, 12]

# Bottom-middle (seconds tens)
# A: GPIO24 B: 8  C: 7  D: 25
lamp5 = [25, 7, 8, 24]

# Bottom-right IC (nearest female connector to Pi; seconds units)
# A: GPIO18 B: 14 C: 15 D: GPIO23
lamp6 = [23, 15, 14, 18]

# Bottom pair of dots
bDots = 26

# Top pair of dots
tDots = 19

lamps = [lamp3, lamp2, lamp1, lamp4, lamp5, lamp6]

for lamp in lamps:
    for pin in lamp:
        GPIO.setup(pin, GPIO.OUT)

GPIO.setup(bDots, GPIO.OUT)
GPIO.setup(tDots, GPIO.OUT)

# ****************************
# Functions start here
# ********************
def showOutput(hrs, mins, secs):
    # Function to illuminate tubes
    # Pass in three pairs of values to appear.
    # Leading zeros are added automatically.
    currDigit = 1
    timeArr = [hrs, mins, secs]
    
    for item in timeArr:
        if item > 9 and item < 100:
            lightUp(currDigit, item // 10)
	    lightUp(currDigit + 1, item - ((item // 10) * 10))
        elif item > 2000:
            # Deals with the clock displaying the date.
            num = item - 2000
            lightUp(currDigit, num // 10)
	    lightUp(currDigit + 1, num - ((num // 10) * 10))

            global tDots
            global bDots
            GPIO.output(tDots, 0)
            GPIO.output(bDots, 1)
            time.sleep(5)
        else:
	    lightUp(currDigit, 0)
	    lightUp(currDigit + 1, item)

        currDigit = currDigit + 2

def cycleNums():
    # Get each tube to show 10 different digits at (pseudo)random, over the space of 1sec.
    print("Cathode protection cycle starting...")
    global tDots
    global bDots
    GPIO.output(tDots, 0)
    GPIO.output(bDots, 0)
    
    for x in range(20):
        for y in range(1, 7):
            lightUp(y, random.randint(0, 9))
            
	time.sleep(0.05)
        
    print("Cathode protection cycle complete.")

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

while True:
    # approximately every ten times per second, update the display

    now = datetime.datetime.now()
    hrs = now.hour
    mins = now.minute
    secs = now.second
    milli = float(now.strftime('%f'))
    
    day = now.day
    month = now.month
    year = now.year

    # Debug output...
    #print("Time: " + str(hrs) + ":" + str(mins) + ":" + str(secs))
    #print("Date: " + str(day) + "/" + str(month) + "/" + str(year))
    #print("----")

    if secs==15 or secs==45:
        # Cycle the tubes through different digits to prevent cathode poisoning.
	cycleNums()    
    elif secs >= 16 and secs <= 20: # or (secs >= 46 and secs <= 50)):
        # Show the date at quarter past each minute for 5s
	showOutput (day, month, year)
    else:
        # Show the time on the tubes.
	showOutput(hrs, mins, secs)
        # Deal with the dots.
        global tDots
        global bDots
        if milli < 500000:
            GPIO.output(tDots, 1)
            GPIO.output(bDots, 1)
        else:
            GPIO.output(tDots, 0)
            GPIO.output(bDots, 0)

    time.sleep(0.1)
