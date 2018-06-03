#from grovepi import *
from sys import *
import numpy as np
import cv2
import pickle

import subprocess
import glob
import os

from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan

setRGB(0,100,0)

button = 7
pinMode(button,"INPUT")

#setRGB(0,255,0)

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train4.yml")

while True:
        try:
                button_status= digitalRead(button)      #Read the Button status
                if button_status:

                    userCount = len([name for name in os.listdir('/home/pi/Desktop/git/image') if os.path.isdir("/home/pi/Desktop/git/image")])
                    print (userCount)
                    userCount +=1
                    usrc = str(userCount)
                    print ("taking picture number " + usrc)
                    setText_norefresh("Adding set of users number " + usrc)
                    if not os.path.exists("/home/pi/Desktop/git/image/"+ repr(userCount)):
                        os.makedirs("/home/pi/Desktop/git/image/"+ repr(userCount))

                    labels = {"persons_name": 1}
                    with open("labels.pkl", 'rb')as f:
                            og_labels = pickle.load(f)
                            labels = {v:k for k,v in og_labels.items()}
                        

                    cap = cv2.VideoCapture(0)
                    
                    faceCounter = 0
                    while(True):
                        # Capture frame-by-frame
                        ret, frame = cap.read()
                        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                        for (x, y, w, h) in faces:
                            #print(x,y,w,h)
                            roi_g = gray[y:y+h, x:x+w]#y cord_start, ycord_end
                            roi_c = frame[y:y+h, x:x+w]

                            #recognise the reason of intrest
                            #using a deep learned model to predict (keras, tensor flow, pytorch, scikit, learn)
                            #

                            
                            if faceCounter == 99:
                                cap.release()
                                cv2.destroyAllWindows()
                                setText_norefresh("User complete. Now adding to system ")
                                subprocess.call('python3 faces-train.py', shell=True)

                            faceCounter = faceCounter +1
                            id_, conf = recognizer.predict(roi_g)
                            img_item = '/home/pi/Desktop/git/image/'+repr(userCount)+'/image'+repr(faceCounter)+'.png'
                            cv2.imwrite(img_item, roi_g)
                            print (faceCounter)
                            faceCount = str(faceCounter)
                            setText_norefresh("Taking number " + faceCount + " of 100")
##                            if faceCounter == 100:
##                                    setText_norefresh("User complete. Now adding to system ")
##                                    subprocess.call('python3 faces-train.py', shell=True)
                            if conf>=45 and conf <=85:        


                                font = cv2.FONT_HERSHEY_SIMPLEX
                                name = labels[id_]
                                color = (255, 0, 0) #In BGRcolor
                                stroke = 2
                                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)



                            

                            #rectangle
                            color = (244, 66 ,167) #In BGRcolor
                            stroke = 2
                            cordx = x + w #width
                            cordy = y + h #height
                            cv2.rectangle(frame, (x, y), (cordx, cordy), color, stroke)


                            
                        cv2.imshow('frame',frame)
                        if cv2.waitKey(20) & 0xFF == ord('q'):
                            break
                else:           #If Button is in Off position, print "Off" on the screen
                        print("off")
                        setText_norefresh("Please press button again")

                        


        except (IOError,TypeError) as e:
                print("Error")

