# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 11:49:07 2016

captures frames to fill the buffer.

@author: sebalander
"""
# %% IMPORTS
import cv2
import time as tm


# %% DECLARATION
def bufferLists(vc, reduced, maxDelay):
    # initialize list
    frames = list()
    times = list()

    rval, frame = vc.read()  # first rame
    if reduced:
        frame = cv2.pyrDown(frame)
    t = tm.time()  # frame time
    frames.append(frame)
    times.append(t)

    rval, frame = vc.read()  # second rame
    if reduced:
        frame = cv2.pyrDown(frame)
    t = tm.time()  # frame time
    frames.append(frame)
    times.append(t)

    # oldest frame has index 0 (first)
    # newest has index -1 (last)

    while(times[-1] - times[0] < maxDelay):
        rval, frame = vc.read()  # new rame
        if reduced:
            frame = cv2.pyrDown(frame)
        t = tm.time()  # frame time
        frames.append(frame)
        times.append(t)

    return frames, times
