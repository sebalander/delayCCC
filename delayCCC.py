# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 13:18:38 2016

Functions to be called by mainOFFline.py.

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
from copy import deepcopy


# %% DECLARATION
def findClosestOff(t, times, delayList):
    '''
    finds de indexes of the closest frames in the buffer and the weghts
    needed to linearly combine those image's pixels
    '''
    tms = np.array(times)
    # absolute times of buffered frames
    tAbs = t - delayList

    # indexes of the buffered frames that came *after* each delay
    # ind-1 are the indexes of the frames *before*
    indPos = np.searchsorted(times, tAbs)

    # Interpolation weights of buffered frames *after*
    tPos = tms[indPos]
    tPre = tms[indPos - 1]
    wPos = (tAbs - tPre) / (tPos - tPre)

    return indPos, wPos


# %% DECLARATION
def delayedFrameOff(t, times, frames, delFrm, masks, delayList):
    '''
    Linearly interpolate between two adyacent frames to give a smoother output.
    '''
    # indexes of frames to use and weights for linear combination
    indPos, wPos = findClosestOff(t, times, delayList)

    for i in range(len(delayList)):
        ind = indPos[i]
        w = wPos[i]
        m = masks[i]
        frmPos = frames[ind]
        frmPre = frames[ind - 1]
        # linear combination
        delFrm[m] = np.uint8(w * frmPos[m] + (1 - w) * frmPre[m])


# %% DECLARATION
def delayMasksOff(frame, d, c):
    '''
    List of masks for each vaue of delay
    '''
    (he, wi, ch) = np.shape(frame)

    line = np.arange(-wi/2, wi/2, 1)
    col = np.arange(-he/2, he/2, 1)

    hDist = np.array([line for i in range(0, he)])
    vDist = np.array([col for i in range(0, wi)]).T
    # delay in seconds for each pixel
    delay = np.sqrt(hDist**2 + vDist**2 + d**2) / c
    # round to 100 values, to control memory requirements
    mi = np.min(delay)
    interval = np.max(delay) - mi
    step = interval/500  # to 1e3 beacause slowmo
    # set discreet steps
    delay = np.round((delay - mi) / step) * step + mi
    maxDelay = 1.2*np.max(delay)  # how much time to buffer

    # %% LIST OF DELAYS
    delayList = deepcopy(delay)
    delayList = delayList.reshape(wi*he)
    delayList = np.sort(delayList)

    keep = delayList[:-1] != delayList[1:]
    delayList = delayList[1:][keep]
    delayList = np.flipud(delayList)  # descending, as times

    # masks for selectig appropiate pixels
    masks = [delay == de for de in delayList]
    # correct for smallest delay
    masks[-1] = delay <= delayList[-1]

    return maxDelay, delayList, delay, masks


# %% DECLARATION
def bufferListsOff(frame, maxDelay):
    '''
    make a list of the fist frames to use
    '''
    times = range(int(maxDelay)+2)

    # just repeat the first frame many times
    frames = list([deepcopy(frame) for i in range(len(times))])

    return frames, times
