# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 09:03:09 2016

@author: sebalander
"""
# %% IMPORTS
import numpy as np
import sys
sys.path.append('./')  # where modules are


# %% DECLARATION
def findClosest(t, times, delayList):
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
