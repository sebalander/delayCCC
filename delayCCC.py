# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

# %% IMPORTS
import numpy as np
import time as tm
import cv2
import matplotlib.pyplot as plt
from copy import deepcopy
import sys


# %% FUNCTIONS
def findClosest(t, times, delayList):
    '''
    finds de indexes of the closest frames in the buffer and the weghts
    needed to linearly combine those images pixels
    '''
    # times of frames measured from now
    t0 = t-np.array(times)

    # index of the buffered frames
    # the index is where the element must be inserted to preserve order
    # i.e. index 86 means that we're beteen frame 85 and 86.
    # Set parametrs such that you never get values 0 or
    # len(t0). Those extreme cases are not considered.
    ind = np.searchsorted(t0[::-1], delayList)[::-1]
#    wei =
    return ind


def delayedFrame(t, times, frames, delFrm, masks, delayList):
    # indexes of frames to use
    ind = findClosest(t, times, delayList)

    for i in range(len(delayList)):
        listInd = ind[i]
        m = masks[i]
        delFrm[m] = frames[listInd][m]


# %% PARAMETERS
c = 1  # speed of light in m/s
d = 0.2  # distance to wall in m
w = 1  # screen width in meters
print "Speed of light", c, "m/s"
print "Distance to wall", d, "m"
print "Screen width", w, "m"

# %% CONECT CAMERA
# Following template from
# http://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-
# using-opencv-and-python#2602410
print "\nOpening camera"
camera_index = 1
cv2.namedWindow("Sin retraso")
vc = cv2.VideoCapture(camera_index)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
    print "Unable to connect to camera"
    sys.exit()

cv2.imshow("Sin retraso", frame)
print "Opened camera", camera_index, rval


# %% CALCULATE DELAYS
print "\nCalculating delays"
# since frame rate is uneven we work with delay measured in seconds, not frames
(he, wi, ch) = np.shape(frame)

line = np.arange(-wi/2, wi/2, 1)
col = np.arange(-he/2, he/2, 1)

k = wi/w  # Conversion factor from meters to pixels
hDist = np.array([line for i in range(0, he)])
vDist = np.array([col for i in range(0, wi)]).T
# delay in seconds for each pixel
delay = np.sqrt(hDist**2 + vDist**2 + (d*k)**2) / (c*k)
# round to 1e-3 sec, to reduce memory requirements
delay = np.round(delay, decimals=3)
maxDelay = 2*np.max(delay)  # how much time to buffer

# to check delay calculated properly (in seconds)
plt.imshow(delay)
# np.min(delay)

# %% LIST OF DELAYS
delayList = deepcopy(delay)
delayList = delayList.reshape(wi*he)
delayList = np.sort(delayList)

keep = delayList[:-1] != delayList[1:]
delayList = delayList[1:][keep]
delayList = np.flipud(delayList)  # descending, as times
# masks for selectig appropiate pixels
masks = [delay == de for de in delayList]
print "Number of masks", len(masks)

# %% BUFFER FIRST FRAMES FOR MAX DELAY
print("\nBuffering first frames")
# initialize list
frames = list()
times = list()

rval, frame = vc.read()  # first rame
t = tm.time()  # frame time
frames.append(frame)
times.append(t)

rval, frame = vc.read()  # second rame
t = tm.time()  # frame time
frames.append(frame)
times.append(t)

# oldest frame has index 0 (first)
# newest has index -1 (last)

while(times[-1] - times[0] < maxDelay):
    rval, frame = vc.read()  # new rame
    t = tm.time()  # frame time
    frames.append(frame)
    times.append(t)
#    print(t, times[-1], times[0])
print "Buffer lists length", len(times), len(frames)

# %% LOOP
delFrm = deepcopy(frame)  # frame to modify
cv2.namedWindow("Con retraso")
print "Running main loop"
while rval:

    # CREATE DELAYED IMAGE
    # GET NEW FRAM, UPDALE LISTS
    print "Reading new frame"
    rval, frame = vc.read()  # new rame
    t = tm.time()  # frame time
    frames.append(frame)
    times.append(t)
    # delete buffered frames if too old
    if times[0] + maxDelay < t:
        del times[0]
        del frames[0]
    print "Buffer lists length", len(times), len(frames)

    # CREATE DELAYED FRAME
    print "Creating delayed frame"
    delayedFrame(t, times, frames, delFrm, masks, delayList)

    # SHOW ONSCREEN
    print "Showing onscreen"
    cv2.imshow("Sin retraso", frame)
    cv2.imshow("Con retraso", delFrm)
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("Con retraso")
cv2.destroyWindow("Sin retraso")
