# coding: utf-8
# author: David Labu

import wumpus_v2
import argparse
import time
import sys


def launch(n, h, a, c):
    '''
    :param n: casillas alto / ancho tablero [n = number]
    :param h: número de hoyos (recomendado n - 2) [h = holes]
    :param a: número de flechas disponible [a = arrow]
    :param c: trucos activados. permite visualziar el mapa
    '''
    try:
        # preparar partida
        print('¡Bienvenido a Hunt The Wumpus!\n')
        if not n:
            print('Introduce el tamaño del tablero.')
            n = wumpus_v2.get_input_number()
        if not h:
            print('Introduce el número de pozos')
            h = wumpus_v2.get_input_number()
        if not a:
            print('Introduce el número de flechas')
            a = wumpus_v2.get_input_number()
        print('Creando Tablero...')
        partida = wumpus_v2.HuntTheWumpus(n, h, a)
        # empezar turnos
        print_delay('''
            *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
            * __          __                                *
            * \ \        / /                                *
            *  \ \  /\  / /   _ _ __ ___  _ __  _   _ ___   *
            *   \ \/  \/ / | | | '_ ` _ \| '_ \| | | / __|  *
            *    \  /\  /| |_| | | | | | | |_) | |_| \__ \  *
            *     \/  \/  \__,_|_| |_| |_| .__/ \__,_|___/  *
            *                            | |                *
            *                            |_|                *
            *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*            
        ''')
        print('\nEntras en la caverna del Wumpus y lo primero que ves es...')
        if c:
            partida.board.print_board()
        while not partida.config.endgame:
            partida.print_perception()
            print('¿qué decides?:\n\t1- Avanzar\n\t2- Girar\n\t3- Atacar\n\t4- Escapar')
            partida.action = wumpus_v2.get_input_number()
            while not 1 <= partida.action <= 4:
                print('¡No puedo hacer nada con eso!')
                print('Estas son tus opciones:\n\t1- Avanzar\n\t2- Girar\n\t3- Atacar\n\t4- Escapar')
                partida.action = wumpus_v2.get_input_number()
            partida.do_action()

    except Exception as e:
        print('[ERROR] Fin de partida! Con su fuerza de voluntad, Wumpus '
              'ha usado el hechizo incontrarestable ' + str(e))
        raise e


def print_delay(cool_string):
    for char in cool_string:
        time.sleep(0.02)
        print_by_sys(char)


def print_by_sys(string):
    sys.stdout.write(string)
    sys.stdout.flush()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--number', help='casillas alto / ancho tablero', type=int, default=None)
    ap.add_argument('-w', '--well', help='número de hoyos', type=int, default=None)
    ap.add_argument('-a', '--arrow', help='número de flechas disponible', type=int, default=None)
    ap.add_argument('-c', '--cheats', help='black sheep wall muestra el mapa', type=int, default=None)
    args = vars(ap.parse_args())
    launch(args['number'], args['well'], args['arrow'], args['cheats'])
    # launch(None, None, None)
