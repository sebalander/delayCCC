# -*- coding: utf-8 -*-
"""
6 Mar 2016

Runs the algorithm for online processing of CCC-like delayed video.

@author: sebalander
"""

# %% IMPORTS
import numpy as np
import cv2
import matplotlib.pyplot as plt
from copy import deepcopy
import sys

from delayCCCOffline import delayedFrameOff
from delayCCCOffline import delayMasksOff
from delayCCCOffline import bufferListsOff

# %% PARAMETERS
videoPath = "maniquies15fps.avi"
reduced = False  # flag to reduce video to half
save = True  # save video
onscreen = True  # to show images and plots

fps = 15  # video frame rate
cm2pix = 5.5 / 16.3  # from cm to pixels
tall = 480 * cm2pix  # height of a person in pixels
d = 50  # distance to wall in pixels

c = 250 / fps  # speed of light in pixels per frame
print "Person height", tall, "pix"
print "Distance to wall", d, "pix"
print "Speed of light", c, "pix/frm"

# %% OPEN VIDEO
print "\nOpening video file"

if onscreen:
    cv2.namedWindow("Sin retraso")
    cv2.namedWindow("Con retraso")

vc = cv2.VideoCapture(videoPath)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
    if reduced:
        frame = cv2.pyrDown(frame)
else:
    rval = False
    print "Unable to connect open video"
    sys.exit()

(height, width, channels) = np.shape(frame)

if onscreen:
    cv2.imshow("Sin retraso", frame)

print "Opened video", videoPath, rval

# Video a guardar
fourcc = cv2.VideoWriter_fourcc(*'XVID')
outCR = cv2.VideoWriter('maniquiesConRetraso.avi',
                        fourcc,
                        15.0,
                        (width, height))

# %% CALCULATE DELAYS
print "\nCalculating delays"
# since frame rate is uneven we work with delay measured in seconds, not frames

maxDelay, delayList, delay, masks = delayMasksOff(frame, d, c)


# %% to check delay calculated properly (in seconds)
if onscreen:
    x = np.arange(width)
    y = np.arange(height)
    X, Y = np.meshgrid(x, y)
    CS = plt.contour(X, Y, delay, 10, colors='k')

#    plt.imshow(delay)
#    plt.title('Curvas de nivel del delay en [frames]')
#    plt.xlabel("x coordinate in image [pixels]")
#    plt.ylabel("y coordinate in image [pixels]")
#    plt.show()

    plt.imshow(frame[:, :, ::-1])
    values = [3.6, 4, 6, 8, 10, 13, 17]
    CS = plt.contour(X, Y, delay, 10, colors='w', V=values)
    plt.clabel(CS, inline=1, fontsize=10, fmt='%.0f')
    plt.xlabel("x coordinate in image [pixels]")
    plt.ylabel("y coordinate in image [pixels]")
    plt.show()

print "Number of masks", len(masks)
print "Minimum delay", np.min(delay)
print "max delay", np.max(delay)

# %% BUFFER FIRST FRAMES FOR MAX DELAY
print("\nBuffering first frames")
# oldest frame has index 0 (first)
# newest has index -1 (last)
frames, times = bufferListsOff(frame, maxDelay)
t = times[-1]  # last frame's time
print "Buffer lists length", len(times), len(frames)


# %% PLOT DELAYS
if onscreen:
    fig, axs = plt.subplots(1, 2, sharey=True)

    ax = axs[0]
    ax.plot(delayList, '.')
    ax.set_title("valores de delay")
    ax.set_ylabel("Tiempo [frames]")
    ax.set_xlabel("indice en lista")

    ax = axs[1]
    ax.plot(t-np.array(times), '.')
    ax.set_title("tiempos de frames en buffer")
    ax.set_xlabel("indice en lista")

    plt.show()

# %% LOOP
delFrm = deepcopy(frame)  # frame to modify
print "Running main loop"
while rval:

    # UPDATE TIME, LISTS
    print "\n\nReading new frame", rval
    if reduced:
        frame = cv2.pyrDown(frame)

    t = t + 1  # frame time
    print "t =", t

    frames.append(frame)
    times.append(t)

    # delete buffered frames if too old
    while times[0] + maxDelay < t:
        del times[0]
        del frames[0]
    print "Buffer lists length", len(times), len(frames)

    # CREATE DELAYED FRAME
    print "Creating delayed frame"
    delayedFrameOff(t, times, frames, delFrm, masks, delayList)

    # SHOW ONSCREEN
    if onscreen:
        print "Showing onscreen"
        cv2.imshow("Sin retraso", frame)
        cv2.imshow("Con retraso", delFrm)

    # SAVE
    if save:
        # Se guarda el resultado
        outCR.write(delFrm)

    # GET NEW FRAME, UPDATE LISTS
    rval, frame = vc.read()  # new rame
    print "\n\nReading new frame", rval

    # STOP
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# %% CLOSE WINDOWS RELEASE VIDEO
vc.release()
outCR.release()

if onscreen:
    cv2.destroyWindow("Con retraso")
    cv2.destroyWindow("Sin retraso")
