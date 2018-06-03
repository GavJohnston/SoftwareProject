import numpy as np
import cv2
import pickle
import picamera
import datetime
import time
import threading
import glob
import os

import smtplib, string, subprocess, time

from flask import Flask, render_template, Response
from camera import VideoCamera


from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan

setRGB(0,0,0)

button = 7
pinMode(button,"INPUT")

button_status= digitalRead(button)

# email packages required
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from subprocess import call

SMTP_USERNAME = 'EMAIL@gmail.com'  # email of the sender

SMTP_RECIPIENT = 'EMAIL@gmail.com' # email of the reciever
SMTP_SERVER = 'smtp.gmail.com'  # SMTP server
SSL_PORT = 465

SMTP_PASSWORD = 'N/A'  # Password of the sender



date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
img_item = ("/home/pi/Desktop/git/takenpictures/" + date +"1.jpg")

##facep_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_profileface.xml')
##
##face1_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')
##face3_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt_tree.xml')
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
##eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
##smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train5.yml")

labels = {"persons_name": 1}
with open("labels.pkl", 'rb')as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}
    

cap = cv2.VideoCapture(0)

#cap.open(192.168.43.212/?action=stream?dummy=param.mjpg):
setText_norefresh('--------')

if button_status == True:
    setRGB(255,0,255)
    setText_norefresh('please wait to add new user')
    subprocess.call('python3 pics.py', shell=True)



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

        id_, conf = recognizer.predict(roi_g)
        if conf>= 40 and conf <= 136 :
            
            print(id_, conf) 
            print(labels[id_])


            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 0, 0) #In BGRcolor
            stroke = 2
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
            
        elif cv2.imwrite(img_item, roi_c):
            newest = max(glob.iglob('takenpictures/*.jpg'), key=os.path.getctime)
            #subprocess.call(['python3', 'main.py'])
            print(newest)
            setRGB(255,255,255)
            setText_norefresh('INTRUDER DETECTED NOTIFYING OWNER')

            TO = SMTP_RECIPIENT
            FROM = SMTP_USERNAME
            msg = MIMEMultipart()
            msg.preamble = 'Rpi Sends image'

            # Attach the image
            fp = open(newest, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)
            msg['subject'] = 'Auomated Email from your Security camera do you know this unknown person detected'

            # Send the email via Gmail
            print("Sending the mail")
            server = smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM, [TO], msg.as_string())
            server.quit()
            print("Mail sent")
            


        

        #rectangle
        color = (244, 66 ,167) #In BGRcolor
        stroke = 2
        cordx = x + w #width
        cordy = y + h #height
        cv2.rectangle(frame, (x, y), (cordx, cordy), color, stroke)
##        #eyes
##        eyes = eye_cascade.detectMultiScale(roi_g)
##        for (ex, ey, ew, eh) in eyes:
##                cv2.rectangle(roi_c, (ex, ey), (ex+ew,ey+eh),(0,255,0),2)
##        #smile
##        smile = smile_cascade.detectMultiScale(roi_g)
##        for (sx, sy, sw, sh) in smile:
##                cv2.rectangle(roi_c, (sx, sy), (sx+sw,sy+sh),(255,255,0),2)
##
##        face1 = face1_cascade.detectMultiScale(roi_g)
##        for (ox, oy, ow, oh) in face1:
##                cv2.rectangle(roi_c, (ox, oy), (ox+ow,oy+oh),(255,255,0),2)
##
##        face3 = face3_cascade.detectMultiScale(roi_g)
##        for (tx, ty, tw, th) in face3:
##                cv2.rectangle(roi_c, (tx, ty), (tx+tw,ty+th),(255,255,0),2)
##
##        facep = facep_cascade.detectMultiScale(roi_g)
##        for (px, py, pw, ph) in facep:
##                cv2.rectangle(roi_c, (px, py), (px+pw,py+ph),(200,255,255),2)

##        #print(x,y,w,h)
##        if not print("unknown", count):
##            img_item = ("/home/pi/Desktop/git/takenpictures/" + date +"1.jpg")
##            cv2.imwrite(img_item, roi_c)
##            newest = max(glob.iglob('takenpictures/*.jpg'), key=os.path.getctime)
##            #print(newest)
        
    cv2.imshow('frame',frame)

   

    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    

  
      #Read the Button status


    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



