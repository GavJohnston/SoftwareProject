import cv2
from PIL import Image
import os
import numpy as np
import pickle
import subprocess

from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan

setRGB(0,255,255)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#where ever the python file is saved to look for the path for itself

image_dir = os.path.join(BASE_DIR, "/home/pi/Desktop/git/image/")
#image directory - take base directory and provide the images



face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()#using lbph face recognizer


current_id = 0
label_ids = {}
x_training = []#empty list list of pickle numbers
y_titles = []#empty list names from number



for root, dirs, files in os.walk(image_dir):
        for file in files:#go through files
                        if file.endswith("png"):#if it ends ion jpg or png
                                path = os.path.join(root, file)
                                label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()#grabs name of directory in order to give it a label/replace spaces with - and make everything lowercase
                                print(label,path)#print out the file path
                                setText_norefresh('Adding user number ' + label + '.Please wait')

                                if not label in label_ids: #if it is in the dictionary 
                                        label_ids[label] = current_id#if the label is equal to the current id
                                        current_id +=1# add it in and give it a current id
                                
                                

                                id_ = label_ids[label]
                                ##print(label_ids)
                                #y_titles.append(label) #some number
                                #x_training.append(path) #verify the image, turn it into a numpy array, gray image
                                pil_image = Image.open(path).convert("L")#grab python image library to get the image and converts into grayscale
                                size = (550, 550)
                                final_image = pil_image.resize(size, Image.ANTIALIAS)
                                image_array = np.array(final_image, "uint8")#convert it into a numpy array 
                                print(image_array)#print array every pixel to numbers

                                #we turn the images into a grayscale and then converted them into a numpy array(numbers)
                                #produced numbers related or in that images, we can then begin to train the image
                                
                                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
                                ##detect the image same as 

                                for(x,y,w,h) in faces:
                                        roi = image_array[y:y+h, x:x+w]#grab reason of intrest get the y value to y + h and the x value to x + h

                                eyes = eye_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
                                ##detect the image
        ##
                                for(ex,ey,ew,eh) in eyes:
                                        roi = image_array[ey:ey+eh, ex:ex+ew]
        ##


                                        x_training.append(roi)#traing with the reason of intrest
                                        y_titles.append(id_)#

        print(y_titles)


        print(x_training)
print("complete")
setText_norefresh('complete')

subprocess.call('python3 faces.py', shell=True)
                        
#adding labels using pickle
with open("labels.pkl", 'wb')as f:#name as pickle, write
        pickle.dump(label_ids, f)# dump the label id




recognizer.train(x_training, np.array(y_titles))#train the training and numpy array of the labels
recognizer.save("train5.yml")#save it in trainner.yml
