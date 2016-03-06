# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 09:14:18 2016

@author: sebalander
"""
# %% IMPORTS
import numpy as np
from copy import deepcopy
import sys
sys.path.append('./')  # where modules are


# %% DECLARATION
def delayMasks(frame, w, d, c):
    (he, wi, ch) = np.shape(frame)

    line = np.arange(-wi/2, wi/2, 1)
    col = np.arange(-he/2, he/2, 1)

    k = wi/w  # Conversion factor from meters to pixels
    hDist = np.array([line for i in range(0, he)])
    vDist = np.array([col for i in range(0, wi)]).T
    # delay in seconds for each pixel
    delay = np.sqrt(hDist**2 + vDist**2 + (d*k)**2) / (c*k)
    # round to 100 values, to control memory requirements
    mi = np.min(delay)
    interval = np.max(delay) - mi
    step = interval/100
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

    return maxDelay, delayList, delay, masks
