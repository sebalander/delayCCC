# -*- coding: utf-8 -*-
"""
Este script agrega retraso temporal a cada fila de pixeles de un video.

Copyright 2016 Sebastian I. Arroyo

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
import sys

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
    retrasosLista = np.arange(np.max(retrasos) + 1)

    # convierto a una matriz con retraso cte dentro de cada fila
    retrasosMatrix = np.array([retrasos for i in range(width)]).T

    # paso a que la mascara sea de tres canales y ordeno las dimensiones
    # retrasosMatrix = np.array([retrasosMatrix, retrasosMatrix, retrasosMatrix])
    # s = np.shape(retrasosMatrix)
    # retrasosMatrix = retrasosMatrix.reshape([s[1],s[2],s[0]])

    # lista de mascaras
    mascarasLista = [retrasosMatrix == retr for retr in retrasosLista]

    return retrasosLista, mascarasLista


# %% DECLARATION
def actualizoListaDeFrames(listaDeFrames, indicesDeFrames, frame, vc, retrasoMax):
    '''
    agrega un frame al final de la lista
    '''
    listaDeFrames = np.append(listaDeFrames, [frame], axis=0);
    indicesDeFrames = np.insert(indicesDeFrames,
                                np.size(indicesDeFrames),
                                vc.get(1))
    # saco los frames viejos
    indicesGuardar = indicesDeFrames + retrasoMax + 1 > np.max(indicesDeFrames)

    return listaDeFrames[indicesGuardar], \
           indicesDeFrames[indicesGuardar]

# %% PARAMETROS
videoName = "videos/apple"
ext = "avi"
reduced = False  # flag para reducir el video a la mitad te tamaño
save = True  # flag para guardar video
onscreen = True  # flag para mostrar resultados en pantalla

DT = 1;  # retraso de la parte inferior respecto a la superior en segundos. La
         # fila inferior se muestra sin retraso

# %% ABRIR ARCHIVO DE VIDEO
print("\nAbriendo archivo de video")

vc = cv2.VideoCapture(videoName+'.'+ext)

if vc.isOpened():  # intentar leer primer frame
    rval, frame = vc.read()
    if reduced:
        frame = cv2.pyrDown(frame)
else:
    rval = False
    print("Unable to connect open video")
    sys.exit()

# lista para guardar los frames y array para los indices
listaDeFrames = np.array([frame])
indicesDeFrames = np.array(vc.get(1),dtype=int)

'''
indices para usa en la funcion get():
CV_CAP_PROP_POS_MSEC =0,
CV_CAP_PROP_POS_FRAMES =1,
CV_CAP_PROP_FRAME_WIDTH =3,
CV_CAP_PROP_FRAME_HEIGHT =4,
CV_CAP_PROP_FPS =5,
CV_CAP_PROP_FOURCC =6,
CV_CAP_PROP_FRAME_COUNT =7,

'''

width = int(vc.get(3))  # cv2.CV_CAP_PROP_FRAME_WIDTH)
height = int(vc.get(4))  # cv2.CV_CAP_PROP_FRAME_HEIGHT)
fps = vc.get(5) # cv2.CV_CAP_PROP_FPS)  # get video frame rate

if onscreen:
    cv2.namedWindow("Sin retraso")
    cv2.namedWindow("Con retraso")
    cv2.imshow("Sin retraso", frame)

print("Opened video", videoName, rval)

# Video a guardar
fourcc = cv2.VideoWriter_fourcc(*'XVID')

outCR = cv2.VideoWriter(videoName+'delayed.avi',
                        fourcc,
                        fps,
                        (width, height))

# %% CALCULO MASCARAS Y LOS RETRASOS ASOCIADOS
retrasosLista, mascarasLista = horizontalMascaras(DT, fps, width, height)
retrasoMax = np.max(retrasosLista)
# %% REGLA GENERAL PARA PONER RETRASOS
# se van guardando los frames leidos y sus índices del video
# a medida que se escribe en el archivo de destino debe cumplirse
# indices de frames leidos + retraso = indice de frame a generar
# Para saber qué indice de frame leído hay que ir a buscar hacemos
# indices de frames leidos = indice de frame a generar - retraso
# a medida que se recorre la lista de retrasos

# CV_CAP_PROP_POS_FRAMES =1

nFrames = vc.get(7) + retrasoMax

# %%
while outCR.get(1) <= nFrames:
    
    rval, frame = vc.read()
    if not rval:
        break

    # actualizo lista de frames con un onuevo
    listaDeFrames, indicesDeFrames = actualizoListaDeFrames(listaDeFrames,
                                                            indicesDeFrames,
                                                            frame,
                                                            vc,
                                                            retrasoMax)

    # compongo frame (aca tambien se eliminan frames de la lista despeusd e usar)
    # usar min y max para elegir adecuadametne los frames en caso de esstar en un extremo.
    indiceActualSalida = np.int(outCR.get(1) + 1)  # indice del frame a generar

    framesParaCadaMascara = indiceActualSalida - retrasosLista
    # rectifico para que este dentro del rango de frames disponibles
    indiceMinimo = np.min(indicesDeFrames)
    indiceMaximo = np.max(indicesDeFrames)
    framesParaCadaMascara[framesParaCadaMascara < indiceMinimo] = indiceMinimo
    framesParaCadaMascara[indiceMaximo < framesParaCadaMascara] = indiceMaximo

    # lo convierto a los índices
    indicesDeFramesParaMascara = [np.where(indicesDeFrames==frm)[0][0] for frm in framesParaCadaMascara]
    frameGenerado = frame.copy()
    print("leyendo frame %d; generando frame %d"%(vc.get(1), outCR.get(1)))

    for i, masc in enumerate(mascarasLista):
        indiceFrameElegido = indicesDeFramesParaMascara[i]
        frameElegido = listaDeFrames[indiceFrameElegido]
        frameGenerado[masc] = frameElegido[masc]

    outCR.write(frameGenerado)
    
    if onscreen:
        cv2.imshow("Con retraso", frameGenerado)
        cv2.imshow("Sin retraso", frame)


# %% CLOSE WINDOWS RELEASE VIDEO
vc.release()
outCR.release()

if onscreen:
    cv2.destroyWindow("Con retraso")
    cv2.destroyWindow("Sin retraso")

