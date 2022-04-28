from itertools import count
import RPi.GPIO as GPIO
import time

#Pin Defs
RedLED = 18 
GrLED = 24

GPIO.setmode(GPIO.BCM)

# Setting mode and initial conditions for Red LED
GPIO.setup(RedLED, GPIO.OUT, initial=GPIO.HIGH)

# Setting mode and initial conditions for green LED
GPIO.setup(GrLED, GPIO.OUT, initial=GPIO.LOW)

while True:
    #start with red on green off
    GPIO.output(RedLED, GPIO.HIGH)
    GPIO.output(GrLED, GPIO.LOW)

    time.sleep(3)
    #switch red off green on
    GPIO.output(RedLED, GPIO.LOW)
    GPIO.output(GrLED, GPIO.HIGH)

    time.sleep(3)
    #switching red and green LED off 
    GPIO.output(RedLED, GPIO.LOW)
    GPIO.output(GrLED, GPIO.LOW)

    time.sleep(3)
    #Loop counter end loop after 50 cycles
    loopnum = 1 + loopnum
    if loopnum == 50:
	    break