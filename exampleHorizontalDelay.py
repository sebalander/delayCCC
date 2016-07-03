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
import sys

# %% PARAMETROS
videoName = "videos/apple"
ext = "avi"

DT = 7;  # retraso de la parte inferior respecto a la superior en segundos. La
         # fila inferior se muestra sin retraso

# %% ABRIR ARCHIVO DE VIDEO
print("\nAbriendo archivo de video")

vc = cv2.VideoCapture(videoName+'.'+ext)

if vc.isOpened():  # intentar leer primer frame
    rval, frame = vc.read()

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

print("Opened video", videoName, rval)

# Video a guardar
fourcc = cv2.VideoWriter_fourcc(*'XVID')

outCR = cv2.VideoWriter(videoName+'delayed'+DT+'s.avi',
                        fourcc,
                        fps,
                        (width, height))

# %% CALCULO RETRASOS 
# REGLA GENERAL PARA PONER RETRASOS
# se van guardando los frames leidos y sus índices del video
# a medida que se escribe en el archivo de destino debe cumplirse
# indices de frames leidos + retraso = indice de frame a generar
# Para saber qué indice de frame leído hay que ir a buscar hacemos
# indices de frames leidos = indice de frame a generar - retraso
# a medida que se recorre la lista de retrasos


m = float(DT)/height  # pendiente de la recta
heights = np.arange(height)  # indice de alturas
retrasos =  DT - m * heights

# convierto a índices de frames
retrasos = np.int16(retrasos * fps + 0.5)

retrasoMax = np.max(retrasos)
retrasosLista =  np.arange(retrasoMax + 1)

# CV_CAP_PROP_POS_FRAMES =1


# %% PRIMER BUCLE, LEYENDO FRAMES DE ARCHIVO
rval, frame = vc.read()
nFrm = 0
while rval:
    nFrm = vc.get(1)    
    
    # agrego nuevo frame al buffer
    listaDeFrames = np.append(listaDeFrames, [frame], axis=0);
    indicesDeFrames = np.insert(indicesDeFrames,
                                np.size(indicesDeFrames),
                                nFrm)
    # saco los frames viejos
    indicesGuardar = indicesDeFrames + retrasoMax > nFrm
    listaDeFrames = listaDeFrames[indicesGuardar]
    indicesDeFrames = indicesDeFrames[indicesGuardar]
    print("frames guardados en buffer",len(listaDeFrames))


    # compongo frame (aca tambien se eliminan frames de la lista despeus de usar)
    indiceActualSalida = np.int(nFrm)  # indice del frame a generar
    framesParaCadaMascara = indiceActualSalida - retrasosLista
    
    # usar min y max para elegir adecuadametne los frames en caso de estar en un extremo.
    # rectifico para que este dentro del rango de frames disponibles
    indiceMinimo = np.min(indicesDeFrames)
    indiceMaximo = np.max(indicesDeFrames)
    framesParaCadaMascara[framesParaCadaMascara < indiceMinimo] = indiceMinimo
    framesParaCadaMascara[indiceMaximo < framesParaCadaMascara] = indiceMaximo

    # lo convierto a los índices
    indicesDeFramesParaMascara = [np.where(indicesDeFrames==frm)[0][0]
                                    for frm in framesParaCadaMascara]:
                                        
    print("Procesando frame %d"%nFrm)
    frameGenerado = frame.copy()
    for i, ret in enumerate(retrasosLista):
        filasAAplicar = retrasos==ret  # podría modificarse el codigo
                                       # para que esta cuenta se haga
                                       # una sola vez al ppio
        frameACopiar = listaDeFrames[indicesDeFramesParaMascara[i]]
        frameGenerado[filasAAplicar,:,:] = frameACopiar[filasAAplicar,:,:]

    outCR.write(frameGenerado)
    
    rval, frame = vc.read()


# %% SEGUNDO BUCLE, APLICANDO LOS FRAMES DEL BUFFER

while len(listaDeFrames)-1:
    nFrm = nFrm + 1    
    
    # saco los frames viejos
    indicesGuardar = indicesDeFrames + retrasoMax > nFrm
    listaDeFrames = listaDeFrames[indicesGuardar]
    indicesDeFrames = indicesDeFrames[indicesGuardar]
    print("frames guardados en buffer",len(listaDeFrames))


    # compongo frame (aca tambien se eliminan frames de la lista despeus de usar)
    indiceActualSalida = np.int(nFrm)  # indice del frame a generar
    framesParaCadaMascara = indiceActualSalida - retrasosLista

    # usar min y max para elegir adecuadametne los frames en caso de estar en un extremo.
    # rectifico para que este dentro del rango de frames disponibles
    indiceMinimo = np.min(indicesDeFrames)
    indiceMaximo = np.max(indicesDeFrames)
    framesParaCadaMascara[framesParaCadaMascara < indiceMinimo] = indiceMinimo
    framesParaCadaMascara[indiceMaximo < framesParaCadaMascara] = indiceMaximo

    # lo convierto a los índices
    indicesDeFramesParaMascara = [np.where(indicesDeFrames==frm)[0][0]
                                    for frm in framesParaCadaMascara]:
                                        
    print("Procesando frame %d"%nFrm)
    for i, ret in enumerate(retrasosLista):
        filasAAplicar = retrasos==ret  # podría modificarse el codigo
                                       # para que esta cuenta se haga
                                       # una sola vez al ppio
        frameACopiar = listaDeFrames[indicesDeFramesParaMascara[i]]
        frameGenerado[filasAAplicar,:,:] = frameACopiar[filasAAplicar,:,:]

    outCR.write(frameGenerado)
    

# %% CLOSE WINDOWS RELEASE VIDEO
vc.release()
outCR.release()


