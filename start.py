from grovepi import *
import subprocess
#from subprocess import call
import os

button = 7
pinMode(button,"INPUT")
originalDir = os.path.dirname('/home/pi/Desktop/git/')
os.chdir('/home/pi/Desktop/git/')
while True:
        try:
                button_status= digitalRead(button)      #Read the Button status
                if button_status:       #If the Button is in HIGH position, run the program
                        subprocess.Popen("python3 pics.py", shell=True)
                        #call('python3 pics.py', shell=True)                                            
                        # run script and print message                  
                else:           #If Button is in Off position, print "Off" on the screen
                        print("off")
                        # print "Off"                   
        except KeyboardInterrupt:       # Stop the buzzer before stopping
                print("keyboardInterrupt")
                break
        except (IOError,TypeError) as e:
                print("Error")
