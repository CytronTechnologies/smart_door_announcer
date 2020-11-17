from pygame import mixer  # Load the popular external library
from datetime import datetime

mixer.init() #Initialize mixer

# Play sound file
# Supporter format: MP3, WAV, OGG
def playSound(file, wait=True):
    #Load sound file and play
    mixer.music.load(file)
    mixer.music.play()
    
    #Wait until music finish playing if "wait" == True
    while(mixer.music.get_busy() and wait):
        continue

# Decide sound to play according to time
def decideSound():
    t = datetime.now() #Get current date and time
    print("Current Time:", t)

    t = (float) (t.strftime("%H.%M")) #Hour and minute
        
    #Play different sounds according to the time
    if(t>=7.00 and t<=9.00): #Morning
        print("Good morning, welcome to Cytron")
        playSound('sounds/morning.mp3', wait=True)
    elif(t>=12.00 and t<=13.30): #Lunch time
        print("It's lunch time!")
        playSound('sounds/lunchtime.mp3', wait=True)
    elif(t>=13.30 and t<=14.30): #End lunch
        print("Do you enjoy your lunch?")
        playSound('sounds/endlunch.mp3', wait=True)
    elif(t>=17.00 and t<=24.00): #Night time
        print("Good evening, have a safe journey home")
        playSound('sounds/evening.mp3', wait=True)
    elif(t>=0.00 and t<=6.00): #Midnight (Security alarm)
        print("Someone is stealing things!")
        playSound('sounds/alarm.mp3', wait=True)
    else: #Other cases
        print("Good day, remember to wash your hands")
        playSound('sounds/other.mp3', wait=True)

