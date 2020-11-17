from sound import *
from motion import *
from pixels import Pixels
import time
import _thread
import argparse
from subprocess import call
import RPi.GPIO as GPIO

#Current state of motion detect
# 0: No motion detected
# 1: Motion detected and remain in frame
state = 0

#RGB LED
pixels = Pixels() #To control the RGB LED

#Indicate program startup
pixels.wakeup()
pixels.speak()
playSound('sounds/piano.mp3')
pixels.off()

#Script parameters
ap = argparse.ArgumentParser()

#Opencv output display must be disabled to run in startup script
ap.add_argument("-nd", "--nodisplay", action="store_false",
                help="Disable opencv output display")
args = vars(ap.parse_args())

#Power off button on top of ReSpeaker Hat
BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

#Function for blinking LED
def ledBlink():
    global pixels
    pixels.wakeup()
    pixels.think()
    time.sleep(8)
    pixels.off()

while True:
    
    #Power off button pressed
    if GPIO.input(BUTTON_PIN) == 0:
        pixels.wakeup()
        pixels.speak()
        playSound('sounds/poweroff.mp3')
        pixels.off()
        time.sleep(3)
        break
    
    motion = detectMotion(args["nodisplay"]) #Detect motion
    state = 0 if motion==0 else state #Update the current motion state
    
    #Motion detected
    if motion==1 and state==0:
         
        _thread.start_new_thread(ledBlink, ()) #Play with LED
        
        decideSound() #Play sound according to time
        
        state = 1 #Update the current motion state

#Shutdown Raspi after poweroff button is pressed
call("sudo poweroff", shell=True)
