# -*- coding: utf-8 -*-
"""
This program applies a delay to the pixels of a video. The delay
is designed so that the output video mimics (though a very simple model)
what an observer should see if light were to travel at much lower speeds
than in reality. This script calls the functions declared in
delayCCCOffline.py.

Copyright (C) 2016 Sebastián I. Arroyo, email: seba.arroyo7@gmail.com.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

@author: sebalander
"""

# %% IMPORTS
import numpy as np
import cv2
import matplotlib.pyplot as plt
from copy import deepcopy
import sys

from delayCCC import delayedFrameOff
from delayCCC import delayMasksOff
from delayCCC import bufferListsOff

# %% LICENSE
print("\
delayCCC Copyright (C) 2016 seba.arroyo7@gmail.com\n\
This program comes with ABSOLUTELY NO WARRANTY.\n\
This is free software, and you are welcome to redistribute it under\n\
the conditions of the GNU General Public License Version 3,\n\
29 June 2007, <http://www.gnu.org/licenses/>.\
")

# %% LICENSE
print("\
delayCCC Copyright (C) 2016 seba.arroyo7@gmail.com\n\
This program comes with ABSOLUTELY NO WARRANTY.\n\
This is free software, and you are welcome to redistribute it under\n\
the conditions of the GNU General Public License Version 3,\n\
29 June 2007, <http://www.gnu.org/licenses/>.\
")

# %% PARAMETERS
videoName = "videos/MVI_6801"
ext = "MOV"
reduced = False  # flag to reduce video to half
save = True  # save video
onscreen = True  # to show images and plots

fps = 120  # video frame rate, "desired"
m2pix = 2 * 320 / 2.0  # from m to pixels
tall = 1.7 * m2pix  # height of a person in pixels
d = 0.5 * m2pix  # distance to wall in pixels, real dist was 2.3m

c = 0.5 * m2pix / fps  # speed of light in pixels per frame
print "Person height", tall, "pix"
print "Distance to wall", d, "pix"
print "Speed of light", c, "pix/frm"

# %% OPEN VIDEO
print "\nOpening video file"

if onscreen:
    cv2.namedWindow("Sin retraso")
    cv2.namedWindow("Con retraso")

vc = cv2.VideoCapture(videoName+'.'+ext)

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

print "Opened video", videoName, rval

# Video a guardar
fourcc = cv2.VideoWriter_fourcc(*'XVID')

outCR = cv2.VideoWriter(videoName+'delayed.avi',
                        fourcc,
                        fps,
                        (width, height))
# to correct for false fps
realVD = cv2.VideoWriter(videoName+'real.avi',
                         fourcc,
                         fps,
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

# %% MAIN LOOP
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
        realVD.write(frame)

    # GET NEW FRAME, UPDATE LISTS
    rval, frame = vc.read()  # new rame
    print "\n\nReading new frame", rval

    # STOP
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# %% CLOSE WINDOWS RELEASE VIDEO
vc.release()
outCR.release()
realVD.release()

if onscreen:
    cv2.destroyWindow("Con retraso")
    cv2.destroyWindow("Sin retraso")
