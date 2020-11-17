from tkinter import *
from tkinter import Tk
import os
from tkinter import filedialog

#Constants
#Before ":" -> For display purpose
#After ":" -> Sound file name (make sure they match in /sounds folder)
SOUNDS = {
    'Morning':'morning',
    'Lunch Time':'lunchtime',
    'End Lunch':'endlunch',
    'Evening':'evening',
    'Other':'other',
    'Alarm':'alarm'
}

#Initialize variables
location = list(SOUNDS.values())[0] #Default value of dropdown menu
command = None #SCP command
filepath = None #Music file path

# Function for opening the file explorer window
def browseFiles():
    global filepath
    filepath = filedialog.askopenfilename(initialdir = ".\/", 
                                          title = "Select a File", 
                                          filetypes = (("MP3 File", 
                                                        "*.mp3*"), 
                                                       ("all files", 
                                                        "*.*"))) 

    # Change label contents
    if not filepath:
        label_file_chosen.configure(text="File Chosen: NONE")
    else:
        filename = os.path.basename(filepath)
        label_file_chosen.configure(text=("File Chosen: " + filename))

#Upload button pressed
def upload():
    global filepath

    if not filepath: #No file selected
        label_log.configure(text="~~Please select a file to upload~~")
    else: #Upload file
        txt = "" #Logging text

        device = entry_device.get()

        #Exectute SCP command
        command = "scp \"" + filepath + "\" pi@" + device + ":~/smart_door_announcer/sounds/" + location + ".mp3"
        out = os.system(command)

        #Display upload results
        if out==0:
            txt = device + ": Success\n"
        else:
            txt = device + ": Failed\n"
        
        if not txt:
            label_log.configure(text="~~Please select destination devices~~")
        else:
            label_log.configure(text=txt)
                                                                                             
# on change dropdown value
def change_dropdown(*args):
    global location
    location = SOUNDS.get(tkvar.get(),'other')

#  Create the root window 
window = Tk() 
   
# Set window title 
window.title('CytronPi Announcer') 
   
#Set window background color 
window.config(background = "white") 

#-----File explorer-----
label_file_chosen = Label(window,  
                            text = "File Chosen: NONE",  
                            fg = "blue") 

button_explore = Button(window,
                        text = "Browse Files",
                        command = browseFiles)
 
entry_device = Entry(window, bg='#e4e6d3')

# Create a Tkinter variable
tkvar = StringVar(window)

# Dictionary with options
choices = SOUNDS
tkvar.set(list(SOUNDS.keys())[0]) # Set default option to first element

popupMenu = OptionMenu(window, tkvar, *choices)

# link function to change dropdown
tkvar.trace('w', change_dropdown)

label_log = Label(window,  
                text = "Output log",
                fg = "red")

button_upload = Button(window,
                        text = "Upload",
                        command = upload)

label_hint = Label(window,  
                text = "Step 1: Click on \"Browse File\"\n\
Step 2: Choose a .mp3 file\n\
Step 3: Enter hostname or IP address\n\
Step 4: Choose sound to change\n\
Step 5: Click on \"Upload\"\n\
Step 6: Enter password in the command prompt", 
                fg = "green")
   
#UI Components placing (5 columns)
label_file_chosen.grid(column = 1, row = 1, columnspan=4)
button_explore.grid(column = 5, row = 1) 

Label(window, text = "Enter hostname or IP-->").grid(column = 1, row = 2, columnspan = 2)
entry_device.grid(column = 3, row = 2, columnspan = 3)

Label(window, text = "Choose Sound-->").grid(column = 1, row = 3)
popupMenu.grid(column = 2, row = 3)
button_upload.grid(column = 5, row = 3)

label_log.grid(column = 1, row = 4, columnspan=5)

label_hint.grid(column = 1, row = 5, columnspan=5)
   
# Let the window wait for any events 
window.mainloop()