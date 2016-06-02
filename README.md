# delayCCC

Se pone un retraso temporal a cada pixel de un video emulando el efecto de que la velocidad de la luz fuera mucho menor a lo que realmente es.

For OpenCV3.0.0-rc1 and Python2.7.9

Sebastián I. Arroyo - Feb 2016

Descripción
-----------
Se levanta video de una webcam y los fotogramas se almacenan en un buffer. En lugar de mostrar la imagen tomada por la camara se muestra una imagen sintetica a partir de los frames guardados en buffer. Esta imagen se contruye tomando selectivamente los pixeles de los fotogramas guardados en buffer. El criterio para seleccinar qué pixeles se toman de cada fotograma relaciona la posición del pixel en la imagen con tiempo que lleva el fotograma en el buffer. En concreto tau = sqrt(r^2 + d^2)/c. tau es el retardo temporal asociado al pixel, r es la distancia del pixel al centro de la imagen y d es la distancia de la camara al plano donde se mueven los objetos.

Para ver un ejemplo del resultado: https://www.youtube.com/watch?v=4IFmES5uJXQ

CCC
---
Este proyecto está inspirado en uno de los espacios del Centro Cultural de la Ciencia en el polo científico tecnológico.

CCC: http://ccciencia.gob.ar/

Video de la actividad: https://www.youtube.com/watch?v=ewwZXRVekKI

Lineas de Mundo
---------------
El efecto de cómo se ve un objeto superluminico está relacionado con velocidades infinitas y viajes hacia el pasado: http://fisica.cab.cnea.gov.ar/estadistica/zanette/papers/ccc.pdf 
