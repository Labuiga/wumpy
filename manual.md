0- Como su nombre indica, este es el camino manual, si este falla ir a bitacora.md

1- Localizar la carpeta de wumpus

    cd wumpus

2- Ejecutar launch.py con los parámetros deseados.)
    
    . venv/bin/activate && python launch.py
    
    . venv/bin/activate && python launch.py -n 3 -w 1 -a 5 -c 0
    
    . venv/bin/activate && python launch.py -n 5 -w 3 -a 5 -c 1
    
    
3- Info parametros:

    :param n: casillas alto / ancho tablero [n = number]
    :param w: número de pozos (recomendado n - 2) [w = well]
    :param a: número de flechas disponible [a = arrow]
    :param c: trucos activados. permite visualizar el mapa [c = cheats]
