#!/usr/bin/python

# Desafio : http://www.programando.org/blog/2013/03/desafio-marzo-slash-abril-adn-forense/
# Rodrigo Chappa - rodrigo.chappa@gmail.com

def initme(res,path):
    if len(res) == 0: 
        for i in range(1002):
         res.append([])
         path.append([])
         res[i] = [ 0 for j in range(1002)]
         path[i] = ["" for j in range(1002)]

# 
# Wrapper a solve(), parametros similares 
#
# retorna ( puntaje, [evidencia,adn,calces] )
#
def solveandtell( caseno, s1, s2, m, res, path, reusecount = 0, lastl2sz = 0 ):
    print "----------------------------------"
    print "Sospechoso", caseno, " ADN:", s2
    # print s1
    # print s2
    # print ""
    s = solve( s1, s2, m, res, path, reusecount, lastl2sz )
    if s[0] > 0:
        print " Mejor calce con puntaje: ", s[0]
        l = max(len(s[1][0]),len(s[1][1]),len(s[1][2]))
        after=""
        if l>75:
            l = 75
            after = " .."
        print " %s%s" % (s[1][0][:l],after)
        print " %s%s" % (s[1][1][:l],after)
        print " %s"   % (s[1][2][:l])

    return s

# 
# s1         : evidencia
# s2         : adn sospechoso
# m          : matriz de puntaje de alineamiento
# res        : res[i][j] guarda el mejor puntaje al considerar el caracter i
#                de la evidencia y caracter j del adn
# path: Marcas en matriz anterior para conocer el mejor camino
# reusecount : Cuantos caracteres tiene el adn actual con el anterior
# lastl2sz   : De que largo era el adn anterior
#
# retorna ( puntaje, [evidencia,adn,calces] )
#
def solve( s1, s2, m, res, path, reusecount = 0, lastl2sz = 0 ):
    # precalcs locales para no perder tiempo en invocacion de cosas "conocidas"
    post = {}
    prev = {}
    for i in ("A","C","G","T"):
        post[i] = m[i]["-"]
        prev[i] = m["-"][i]

    # llenar la ultima fila y la ultima columna
    # calcular cuanto seria el valor si no hubiera ya elementos del otro string por revisar
    l1 = len(s1)
    l2 = len(s2)
    sum = 0;
    i = l1;
    for j in xrange(l2-1,-1,-1):  # l2-1 down to 0
        sum += prev[s2[j]]
        # print i, j, " ", sum
        res[i][j] = sum

    initcol = True
    # Cuando se calcula manteniendo fija las columnas
    # existe una oportunidad para utilizar reusecount, si este valor es > 0
    # Es > 0 cuando un proceso externo se ha dado cuenta que los ultimos caracteres del string s2 
    # son iguales que los de la ultima vez. Si es asi, los ultimas columnas de la tabla res pueden
    # reutilizarse
    if reusecount > 0 and lastl2sz > 0:
        srcleft  = lastl2sz - reusecount
        srcright = lastl2sz
        dstleft  = l2 - reusecount
        dstright = l2

        # copiaremos datos previos solo si no hay problemas de overlap
        if srcleft <= dstleft or srcleft > dstright:
            initcol = False
            if srcleft != dstleft:
                # print "copiare a ", [dstleft,dstright], "desde", [srcleft,srcright]
               for i in xrange(l1):
                   for j in xrange(srcright,srcleft-1,-1):
                       delta = j-srcleft
                       # print "copiando a ", [i,dstleft+delta], " (", res[i][j],") desde ", [i,j]
                       res[i][dstleft+delta] = res[i][j]
                       path[i][dstleft+delta] = path[i][j]

    # initcol = True
    if initcol:
       sum = 0
       j = l2
       for i in xrange(l1-1,-1,-1): # l1-1 down to 0
           sum += post[s1[i]]
           # print  i , " " , j , " " , sum
           res[i][j] = sum;

    res[l1][l2] = 0;

    lastj = l2-1
    if initcol == False:
        lastj = l2-reusecount-1

    for i in xrange(l1-1,-1,-1): # l1-1 down to 0
        for j in xrange(lastj,-1,-1):  # lastj down to 0
            s1i = s1[i]
            s2j = s2[j]
            if s1i == s2j:
                # premio por ser iguales
                res[i][j] = m[s1i][s1i] + res[i+1][j+1];
                # print i, j, res[i][j]
                path[i][j] = "=";
            else:
                # no son iguales, elegir entre las 3 opciones restantes, la de mayor valor
                opt1 = res[i+1][j] + post[s1i]  # m[s1i]["-"];
                opt2 = res[i][j+1] + prev[s2j]  # m["-"][s2j];
                mx = opt1;
                if opt1 > opt2:
                    path[i][j] = "v"
                else:
                    path[i][j] = ">";
                    mx = opt2;

                opt3 = res[i+1][j+1] + m[s1i][s2j];
                if opt3 > mx:
                    path[i][j] = "\\";
                    mx = opt3;
                # print "Comparing " , opt1 , " " , opt2 , " " , opt3, " max = ", max
                res[i][j] = mx;
                # print i , " " , j , " " , res[i][j]

    # Fin, ahora un poco de administracion.
    # En res[0][0] se encuentra el valor maximo requerido
    # En path[i][j] las decisiones tomadas en cada nivel

    # Mostrar la matriz de resultados parciales?
    if False: # True:
     print
     for i in range(l1+1):
        for j in range(l2+1):
            print "%3d" % res[i][j],
        print

     print
     for i in range(l1+1):
        for j in range(l2+1):
            print path[i][j],
        print

     print

    path1 = path2 = path3 = ""
    # Comentar para ahorrarse la generacion del path
    path1,path2,path3 = rebuildpath(path,s1,s2)

    return res[0][0], [path1,path2,path3]

def rebuildpath(path,s1,s2):
    # rebuild path
    i = 0; j = 0
    path1 = ""  # evidencia + "-" intermedios
    path2 = ""  # adn + "-" intermedios
    path3 = ""  # identifica calces exactos
    l1 = len(s1)
    l2 = len(s2)
    while i < l1 and j < l2:
        p3 = " "
        if path[i][j] == "=" or path[i][j] == "\\":
              path1 += s1[i]
              path2 += s2[j]
              if path[i][j] == "=": p3 = "^"
              i += 1
              j += 1
        elif path[i][j] == "v":
              path1 += s1[i]
              path2 += "-"
              i += 1
        elif path[i][j] == ">":
              path1 += "-"
              path2 += s2[j]
              j += 1
        path3 += p3
    while i < l1:
        path1 += s1[i]
        path2 += "-"
        i += 1

    while j < l2:
        path1 += "-"
        path2 += s2[j]
        j += 1

    return [path1,path2,path3]

# Tomado y modificado desde https://github.com/vramiro/secuencias.git
def parsef(fname):
    m = {'A':None,'C':None,'G':None, 'T':None, '-':None}; suspects = {}; evidence = None
    for l in open(fname).readlines():
        l = l.strip()
        if(l.startswith('#')):
            continue
        (id, rest) = l.split(":")
        ids = ['A', 'C', 'G', 'T', '-']
        if(id in ids):
            l = rest.split(",")
            m[id] = {}
            for i in range(len(l)):
                if l[i] == "*":
                    m[id][ids[i]] = -9999999
                else:
                    m[id][ids[i]] = int(l[i])
        elif(id == '0'):
            evidence = rest
        else:
            suspects[id] = rest
    return (m, evidence, suspects)

def calcval(s1,s2,m):
    print "calcval('%s','%s')" % (s1,s2)
    print s1
    print s2
    print
    if len(s1) != len(s2): return

    v = 0
    for i in range(len(s1)):
        print s1[i], ":", s2[i], "=", m[s1[i]][s2[i]], " ",
        v += m[s1[i]][s2[i]]

    return v

# main, esqueleto original tomado de https://github.com/vramiro/secuencias.git

import sys
(M, evidence, suspects) = parsef(sys.argv[1])
maxv = -float('Inf'); index = 0; adn = None
lastadn = ""

res = []
path = []
initme( res, path )

# ordenar los ADN para que aparezcan ordenados de acuerdo al final del 
# string, con la idea de aprovechar la informacion contenida en arreglo
# res de la iteracion anterior.
for x in sorted(suspects.iteritems(), key=lambda x: x[1][::-1]):
    key = x[0]
    suspect = x[1]
    # descubrir el nro de caracteres que calzan entre el ultimo adn y el
    # actual (contando desde el ultimo hacia el primero)
    rptcnt = 0
    lastadnsz = len(lastadn)
    i = lastadnsz-1
    j = len(suspect)-1
    while i > 0 and j > 0 and lastadn[i] == suspect[j]:
        i -= 1
        j -= 1
        rptcnt += 1
    # print "Caracteres iguales ", rptcnt
    lastadn = suspect

    aux = solveandtell(key,evidence, suspect, M, res, path, rptcnt, lastadnsz )

    # Para comprobar que la optimizacion (de contar los caracteres iguales
    # para no recalcular las ultimas columnas) esta bien sirve invocar 
    # con parametro 0 en rptcnt para que las ultimas columnas sean
    # recalculadas siempre. Luego se comparan los resultados. 
    #aux2 = solveandtell(key,evidence, suspect, M, res, path, 0, 0 )
    #assert(aux==aux2)

    val = aux[0]
    if(val>maxv):
        index = key
        maxv = val
        adn = aux[1]

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "  El culpable es el sospechoso numero %s (%s) con valor %d" % (index, suspects[index], maxv)
print ""
print "Evidencia  |%s|" % adn[0]
print "ADN        |%s|" % adn[1]
print "Calces      %s" % adn[2]
# print calcval( adn[0], adn[1], M )
