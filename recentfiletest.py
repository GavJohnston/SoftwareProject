import glob
import os

newest = max(glob.iglob('/home/pi/Desktop/git/takenpictures/*.jpg'), key=os.path.getctime)


print(newest)
