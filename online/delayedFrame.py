# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 09:04:27 2016

@author: sebalander
"""
# %% IMPORTS
import numpy as np
import sys
sys.path.append('./')  # where modules are

from findClosest import findClosest


# %% DECLARATION
def delayedFrame(t, times, frames, delFrm, masks, delayList):
    # indexes of frames to use and weights for linear combination
    indPos, wPos = findClosest(t, times, delayList)

    for i in range(len(delayList)):
        ind = indPos[i]
        w = wPos[i]
        m = masks[i]
        frmPos = frames[ind]
        frmPre = frames[ind - 1]
        # linear combination
        delFrm[m] = np.uint8(w * frmPos[m] + (1 - w) * frmPre[m])
