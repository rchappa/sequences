sequences
=========

Solucion a problema de secuencias de ADN propuesto en 
http://www.programando.org/blog/2013/03/desafio-marzo-slash-abril-adn-forense/

Usese asi
<pre>
python seq.py input.txt
</pre>

El parsing del archivo y el esqueleto original fue tomado desde
https://github.com/vramiro/secuencias

solve() construye una tabla de solución usando dynamic programming.

Se ordenan los datos para tomar partido de la repeticion de finales de secuencias que hace que la tabla no tenga que recalcular sus ultimas columnas.

Al ejecutarlo, se muestra una salida parecida a esto:

<pre>
$ cat input.txt 
# Matriz
A:5,-1,-2,-1,-3
C:-1,5,-3,-2,-4
G:-2,-3,5,-2,-2
T:-1,-2,-2,5,-1
-:-3,-4,-2,-1,*
          # Evidencia
0:AGTGATG
          # ADN Sospechosos
1:AAATGC
2:AGGAA
3:AGTGATA
4:GATTACA
</pre>

(Se muestra, para cada sospechoso, cual configuracion tiene el mayor puntaje, y se destacan los calces exactos)
<pre>
$ python seq.py input.txt 
----------------------------------
Sospechoso 2  ADN: AGGAA
 Mejor calce con puntaje:  16
 AGTGATG
 AG-GA-A
 ^^ ^^  
----------------------------------
Sospechoso 4  ADN: GATTACA
 Mejor calce con puntaje:  5
 -AGTGATG
 GA-TTACA
  ^ ^ ^  
----------------------------------
Sospechoso 3  ADN: AGTGATA
 Mejor calce con puntaje:  28
 AGTGATG
 AGTGATA
 ^^^^^^ 
----------------------------------
Sospechoso 1  ADN: AAATGC
 Mejor calce con puntaje:  11
 AGTGATG-
 A--AATGC
 ^   ^^^
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  El culpable es el sospechoso numero 3 (AGTGATA) con valor 28

Evidencia  |AGTGATG|
ADN        |AGTGATA|
Calces 
</pre>
(Al final se muestra quien es el "culpable", aquel sospechoso que obtuvo mas puntaje)
