# Nixie Pi clock, v0.1
import datetime, random, time
import RPi.GPIO as GPIO
import feedparser

GPIO.setmode(GPIO.BCM) # I.e. the 5V pin in the top-left corner is referred to as 2.
GPIO.setwarnings(False)

bbcWeather = "2643029"
maxDotBright = 100   # Maximum brightness (100max) of INS-1 dots.

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
pbDots = GPIO.PWM(bDots, 50)
ptDots = GPIO.PWM(tDots, 50)

weatherOk = False   # Did the weather work the last time we tried to get it?
# ****************************
# Functions start here
# ********************

def weather(areaCode):
    url = "https://weather-broker-cdn.api.bbci.co.uk/en/observation/rss/" + areaCode
    
    global ptDots, pbDots, weatherOk

    try:
        NewsFeed = feedparser.parse(url)
        entry = NewsFeed.entries[0]
        weatherString = entry.description
        tempStart = weatherString.find(" ") + 1
        tempEnd = weatherString.find("C") - 1
        temperature = int(weatherString[tempStart:tempEnd])

        humidStart = weatherString.find("Humidity: ") + 9
        humidEnd = weatherString.find("%")
        humidity = int(weatherString[humidStart:humidEnd])
        print("Temp: " + str(temperature) + ". H:" + str(humidity) + ".")
        weatherOk =  True
        pbDots.start(0)
        ptDots.start(0)
        showOutput(humidity, -1, abs(temperature))
        return True
    except:
        # No weather data available.
        weatherOk = False
        return False

def pressure(areaCode):
    url = "https://weather-broker-cdn.api.bbci.co.uk/en/observation/rss/" + areaCode
    
    global ptDots, pbDots, weatherOk

    if 5>4:
        NewsFeed = feedparser.parse(url)
        entry = NewsFeed.entries[0]
        weatherString = entry.description
        pressStart = weatherString.find("Pressure: ") + 10
        pressEnd = weatherString.find("mb")
        pressure = weatherString[pressStart:pressEnd]

        if len(pressure) < 4:
            pressure = "0" + pressure
            
        weatherOk =  True
        pbDots.start(0)
        ptDots.start(0)

        # Show the air pressure on the display.
        lightUp(1, -1)

        if int(pressure) >= 1000:
            lightUp(2, 1)
        else:
            lightUp(2, -1)

        lightUp(3, int(pressure[1:2]))
        lightUp(4, int(pressure[2:3]))
        lightUp(5, int(pressure[3:4]))
        lightUp(6, -1)
        return True
    
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

            global ptDots, pbDots
            global maxDotBright
            pbDots.start(maxDotBright)
            ptDots.start(0)
        elif item >= 0:
	    lightUp(currDigit, 0)
	    lightUp(currDigit + 1, item)
        else:
            # If we're here, we've been sent something like -1.
            lightUp(currDigit, -1)
	    lightUp(currDigit + 1, -1)

        currDigit = currDigit + 2

def slideOff(hrs, mins, secs):
    # Makes current time 'slide off' the display.
    timeArr = [hrs, mins, secs]
    y = 6
    for x in range(1, -7, -1):
        currDigit = x
        for item in timeArr:
            if item > 9 and item < 100:
                lightUp(currDigit, item // 10)
	        lightUp(currDigit + 1, item - ((item // 10) * 10))
            elif item > 2000:
                # Deals with the clock displaying the date.
                num = item - 2000
                lightUp(currDigit, num // 10)
	        lightUp(currDigit + 1, num - ((num // 10) * 10))
            else:
	        lightUp(currDigit, 0)
	        lightUp(currDigit + 1, item)
                
            currDigit = currDigit + 2
            
        # Blank the right-most digits.
        for n in range(6, y, -1):
            lightUp(n, 10)
        y = y - 1
        
        time.sleep(0.1)

    # Then, do something similar to slide the date onto the display.
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    year = now.year
    timeArr = [day, month, year]

    for x in range(6, 0, -1):
        currDigit = x
        for item in timeArr:
            if item > 9 and item < 100:
                lightUp(currDigit, item // 10)
	        lightUp(currDigit + 1, item - ((item // 10) * 10))
            elif item > 2000:
                # Deals with the clock displaying the date.
                num = item - 2000
                lightUp(currDigit, num // 10)
	        lightUp(currDigit + 1, num - ((num // 10) * 10))
            else:
	        lightUp(currDigit, 0)
	        lightUp(currDigit + 1, item)
                
            currDigit = currDigit + 2
        
        time.sleep(0.1)    

def cycleNums():
    # Get each tube to show 10 different digits at (pseudo)random, over the space of 1sec.
    print("Cathode protection cycle starting...")
    
    for x in range(20):
        for y in range(1, 7):
            lightUp(y, random.randint(0, 9))
            
	time.sleep(0.05)
        
    print("Cathode protection cycle complete.")

def cycleNums2():
    # Get each tube to show 10 different digits at (pseudo)random, over the space of 1sec.
    print("Cathode protection cycle starting...")

    now = datetime.datetime.now()
    hrs = now.hour
    mins = now.minute
    secs = now.second + 1  # It takes about a second to do the animation.
    timeArr = [hrs, mins, secs]
    
    startAt = 1
    endAt = 2

    for digits in range(9):
        for x in range(10):
            currDigit = 1    
            for item in timeArr:
                if item > 9 and item < 100 and currDigit < endAt:
                    lightUp(currDigit, item // 10)
	            lightUp(currDigit + 1, item - ((item // 10) * 10))
                else:
                    if currDigit < endAt:
	                lightUp(currDigit, 0)
	                lightUp(currDigit + 1, item)
                currDigit = currDigit + 2
            
            for lamp in range(startAt, endAt):
                lightUp(lamp, random.randint(0, 9))
	    time.sleep(0.015)
            
        endAt = endAt + 1
        if endAt > 4:
            startAt = startAt + 1

    print("Cathode protection cycle complete.")

def lightUp(lamp, numToShow):
    global lamps
    # Pass in which Nixie tube (1-6) and the digit to show (0 to 9)
    # Showing a digit where the value is >9 turns it off, when using the K155ID1 IC.
    if lamp > 0 and lamp < 7:
        lamp = lamp - 1

        if numToShow >= 0 and numToShow <= 9:
            binNum = str(bin(numToShow))[2:]   # binNum will be something like '10'
            #print("numToShow is " + str(numToShow) + " on lamp " + str(lamp) + ".")

            while len(binNum) < 4:  # Add leading zeroes to get it to 4 bits.
                binNum = '0' + binNum 
        
            GPIO.output(lamps[lamp][0], int(binNum[0]))
            GPIO.output(lamps[lamp][1], int(binNum[1]))
            GPIO.output(lamps[lamp][2], int(binNum[2]))
            GPIO.output(lamps[lamp][3], int(binNum[3]))    
            # print("Lamp " + str(lamp + 1) + " showing " + str(numToShow))
        else:
            GPIO.output(lamps[lamp][0], 1)
            GPIO.output(lamps[lamp][1], 1)
            GPIO.output(lamps[lamp][2], 1)
            GPIO.output(lamps[lamp][3], 1)
            # Turn the lamp in question off if < 0 or > 9 is received.
            

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

    if secs==15:
        # Cycle the tubes through different digits to prevent cathode poisoning.
        pbDots.start(0)
        ptDots.start(0)
        slideOff(hrs, mins, secs)
    elif secs==20:
        pbDots.start(0)
        ptDots.start(0)
        cycleNums2()
    elif secs >= 16 and secs <= 20: # or (secs >= 46 and secs <= 50)):
        # Show the date at quarter past each minute for 5s
        #pbDots.start(0)
        #ptDots.start(0)
	showOutput (day, month, year)
    elif (secs==45 or secs == 52) and weatherOk == True:
        pbDots.start(0)
        ptDots.start(0)
        cycleNums()
    elif secs > 45 and secs <52:
        # Show the local humidity (left) and temperature (right)
        if secs > 45 and secs < 49:
            ok = weather(bbcWeather)
        else:
            ok = pressure(bbcWeather)
        
        if ok == False:
            # If the RSS feed isn't working, just keep showing the time,
	    showOutput(hrs, mins, secs)
            # Deal with the dots...
            duty = int((milli / 999999) * maxDotBright)
            if milli < 500000:
                pbDots.start(duty)
                ptDots.start(duty)
            else:
                pbDots.start(maxDotBright - duty)
                ptDots.start(maxDotBright - duty)
    else:
        # Show the time on the tubes.
	showOutput(hrs, mins, secs)
        # Deal with the dots...
        duty = int((milli / 999999) * maxDotBright)
        if milli < 500000:
            pbDots.start(duty)
            ptDots.start(duty)
        else:
            pbDots.start(maxDotBright - duty)
            ptDots.start(maxDotBright - duty)

    #time.sleep(0.05)
