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
sys.path.append('./')  # where modules are

from delayedFrame import delayedFrame
from delayMasks import delayMasks
from bufferLists import bufferLists

# %% PARAMETERS
reduced = True  # flag to reduce video to half
save = True  # save video
onscreen = False  # to show images and plots
c = 0.2  # speed of light in meters/second
d = 2.5/10  # distance to wall in meters
w = 1.3  # screen width in meters
print "Speed of light", c, "m/s"
print "Distance to wall", d, "m"
print "Screen width", w, "m"

# %% CONECT CAMERA
# Following template from
# http://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-
# using-opencv-and-python#2602410
print "\nOpening camera"
camera_index = 1

if onscreen:
    cv2.namedWindow("Sin retraso")
    cv2.namedWindow("Con retraso")

vc = cv2.VideoCapture(camera_index)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
    if reduced:
        frame = cv2.pyrDown(frame)
else:
    rval = False
    print "Unable to connect to camera"
    sys.exit()

(width, height, channels) = np.shape(frame)

if onscreen:
    cv2.imshow("Sin retraso", frame)

print "Opened camera", camera_index, rval

# Video a guardar
fourcc = cv2.VideoWriter_fourcc(*'XVID')
outCR = cv2.VideoWriter('conRetraso.avi',
                        fourcc,
                        3.5,
                        (height, width))
outSR = cv2.VideoWriter('sinRetraso.avi',
                        fourcc,
                        3.5,
                        (height, width))

# %% CALCULATE DELAYS
print "\nCalculating delays"
# since frame rate is uneven we work with delay measured in seconds, not frames

maxDelay, delayList, delay, masks = delayMasks(frame, w, d, c)

# to check delay calculated properly (in seconds)
if onscreen:
    plt.imshow(delay)

np.min(delay), np.max(delay)
print "Number of masks", len(masks)

# %% BUFFER FIRST FRAMES FOR MAX DELAY
print("\nBuffering first frames")
# oldest frame has index 0 (first)
# newest has index -1 (last)
frames, times = bufferLists(vc, reduced, maxDelay)
t = times[-1]  # last frame's time
print "Buffer lists length", len(times), len(frames)


# %% PLOT DELAYS
if onscreen:
    fig, axs = plt.subplots(1, 2, sharey=True)

    ax = axs[0]
    ax.plot(delayList, '.')
    ax.set_title("delays")

    ax = axs[1]
    ax.plot(t-np.array(times), '.')
    ax.set_title("times")

    plt.show()

# %% LOOP
delFrm = deepcopy(frame)  # frame to modify
print "Running main loop"
while rval:

    # GET NEW FRAME, UPDALE LISTS
    print "\n\nReading new frame"
    rval, frame = vc.read()  # new rame
    if reduced:
        frame = cv2.pyrDown(frame)
    t = tm.time()  # frame time
    frames.append(frame)
    times.append(t)
    # delete buffered frames if too old
    while times[0] + maxDelay < t:
        del times[0]
        del frames[0]
    print "Buffer lists length", len(times), len(frames)
    print "Frame Rate", 1.0 / (t - times[-2])

    # CREATE DELAYED FRAME
    print "Creating delayed frame"
    delayedFrame(t, times, frames, delFrm, masks, delayList)

    # SHOW ONSCREEN
    if onscreen:
        print "Showing onscreen"
        cv2.imshow("Sin retraso", frame)
        cv2.imshow("Con retraso", delFrm)

    # SAVE
    if save:
        # Se guarda el resultado
        outSR.write(frame)
        outCR.write(delFrm)

    # STOP
    key = cv2.waitKey(1)
    if key == 27:  # exit on ESC
        break

# %% CLOSE WINDOWS RELEASE VIDEO
vc.release()
outCR.release()
outSR.release()

if onscreen:
    cv2.destroyWindow("Con retraso")
    cv2.destroyWindow("Sin retraso")
