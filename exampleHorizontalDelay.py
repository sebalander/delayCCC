# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 09:44:55 2016

Agrega retraso temporal a cada fila de pixeles de un video.

@author: sebalander

indices para usa en la funcion get():
CV_CAP_PROP_POS_MSEC =0,
CV_CAP_PROP_POS_FRAMES =1,
CV_CAP_PROP_FRAME_WIDTH =3,
CV_CAP_PROP_FRAME_HEIGHT =4,
CV_CAP_PROP_FPS =5,
CV_CAP_PROP_FOURCC =6,
CV_CAP_PROP_FRAME_COUNT =7,

"""
# %% IMPORTS
import numpy as np
import cv2
import matplotlib.pyplot as plt
from copy import deepcopy
import sys

# %% DECLARATION
#def delayedFrameOff(t, times, frames, delFrm, masks, delayList):
#    # indexes of frames to use and weights for linear combination
#    indPos, wPos = findClosestOff(t, times, delayList)
#
#    for i in range(len(delayList)):
#        ind = indPos[i]
#        w = wPos[i]
#        m = masks[i]
#        frmPos = frames[ind]
#        frmPre = frames[ind - 1]
#        # linear combination
#        delFrm[m] = np.uint8(w * frmPos[m] + (1 - w) * frmPre[m])
#
#
# %% DECLARACION
def horizontalMascaras(DT, fps, width, height):
    '''
    List of masks
    '''
    # vector con el retraso de cada fila en segundos.
    # fila 0 -> retraso DT
    # ultima fila -> retraso 0
    m = float(DT)/height  # pendiente de la recta
    heights = np.arange(height)  # indice de alturas
    retrasos =  DT - m * heights
    
    # convierto a índices de frames
    retrasos = np.int16(retrasos * fps + 0.5)

    # convierto a una matriz de retraso cte dentro de cada fila
    retrasosMatrix = np.array([retrasos for i in range(width)]).T
    
    # lista de mascaras
    mascaras = [retrasosMatrix == retr for retr in retrasos]

    return retrasos, mascaras


## %% DECLARATION
#def bufferListsOff(frame, maxDelay):
#    '''
#    make a list of the fist frames to use
#    '''
#    times = range(int(maxDelay)+2)
#
#    # just repeat the first frame many times
#    frames = list([deepcopy(frame) for i in range(len(times))])
#
#    return frames, times


# %% PARAMETROS
videoName = "videos/apple"
ext = "avi"
reduced = False  # flag para reducir el video a la mitad te tamaño
save = True  # flag para guardar video
onscreen = True  # flag para mostrar resultados en pantalla

DT = 1;  # retraso de la parte inferior respecto a la superior en segundos. La
         # fila inferior se muestra sin retraso

# %% ABRIR ARCHIVO DE VIDEO
print "\nAbriendo archivo de video"

vc = cv2.VideoCapture(videoName+'.'+ext)

if vc.isOpened():  # intentar leer primer frame
    rval, frame = vc.read()
    if reduced:
        frame = cv2.pyrDown(frame)
else:
    rval = False
    print "Unable to connect open video"
    sys.exit()

width = int(vc.get(3))  # cv2.CV_CAP_PROP_FRAME_WIDTH)
height = int(vc.get(4))  # cv2.CV_CAP_PROP_FRAME_HEIGHT)
fps = vc.get(5) # cv2.CV_CAP_PROP_FPS)  # get video frame rate

if onscreen:
    cv2.namedWindow("Sin retraso")
    cv2.namedWindow("Con retraso")
    cv2.imshow("Sin retraso", frame)

print "Opened video", videoName, rval

# Video a guardar
fourcc = cv2.VideoWriter_fourcc(*'XVID')

outCR = cv2.VideoWriter(videoName+'delayed.avi',
                        fourcc,
                        fps,
                        (width, height))

# %% CALCULO MASCARAS
retrasos, mascaras = horizontalMascaras(DT, fps, width, height)

retrasoMaximo = np.max(retrasos)

# %% PRIMERA ETAPA, RELLENO DONDE FALTA AL PPIO
# CV_CAP_PROP_POS_FRAMES =1

# el primer frame ya fue generado
while vc.get(1) <= retrasoMaximo:
    frameGenerado = frame

# %% SEGUNDA ETAPA
# CV_CAP_PROP_POS_FRAMES =1
# CV_CAP_PROP_FRAME_COUNT =7

while vc.get(1) <= vc.get(7) - retrasoMaximo:
    frameGenerado = 

# %% TERCERA ETAPA, RELLENO DONDE FALTA AL FINAL
while vc.get() <= retrasoMaximo:
    frameGenerado = 