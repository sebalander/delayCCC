# delayCCC

Se pone un retraso temporal a cada pixel de un video para crear un video donde las imagenes se mueven más rapido que la luz.

For OpenCV3.0.0-rc1 and Python2.7.9

Sebastián I. Arroyo - Mayo 2016

Archivos
--------
- exampleHorizontalDelay.py : script que procesa el video.
- LICENSE : Licencia que rige sobre este software: GNU GPLv3.

Descripción
-----------
Se lee un video de un archivo y a medida que se leen los fotogramas se va generando un video donde las filas horizontales de pixeles tienen un retraso tempral respecto al video original. El retraso es máximo en la fila de arriba y cero en la fila de abajo y va lineal con la altura en la imagen.

Para ver un ejemplo del resultado: https://www.youtube.com/watch?v=4IFmES5uJXQ

CCC
---
Este proyecto está inspirado en uno de los espacios del Centro Cultural de la Ciencia en el Polo Científico Tecnológico visitado en Febrero de 2016.

CCC: http://ccciencia.gob.ar/

Video de la actividad: https://www.youtube.com/watch?v=ewwZXRVekKI

Lineas de Mundo
---------------
El efecto de cómo se ve un objeto superluminico está relacionado con velocidades infinitas y viajes hacia el pasado: <http://fisica.cab.cnea.gov.ar/estadistica/zanette/papers/ccc.pdf>
