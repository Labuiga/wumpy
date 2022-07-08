# coding: utf-8
# author: David Labu

import random


class HuntTheWumpus:
    def __init__(self, n, h, a):
        self.config = Configuration(n, h, a)

        self.board = Board(self.config)

        self.player = Player(self.config, self.board)

        self.fill_board()

        self.gold = None
        self.wumpus_position = None
        self.death_wumpus = None
        self.codex = {0: '¡¡¡Te has encontrado de frente con el Wumpus y no te ha matado porque está durmiendo!!!',
                      1: 'Hueles el Hedor del Wumpus. Avanza con cuidado',
                      2: 'Un hueco donde antes había un tesoro',
                      3: 'Percibes un resplandor dorado',
                      4: '¡¡¡Estas flotando sobre un pozo!!!',
                      5: 'Sientes una brisa, El aire no está tan viciado por aquí',
                      6: 'Estás en la puerta de Entrada, detrás de ti está la salida, '
                         'más huir sin el tesoro no es una opción para un aventurero'}
        self.action = 0

    '''Métodos GamePlay'''
    # Fase 0 turno
    def print_perception(self):
        d = {0: 'norte \u2191', 1: 'oeste \u2190', 2: 'este \u2192', 3: 'sur \u2193'}
        f = 'flechas' if self.player.arrows > 1 else 'flecha'
        t = f'\tLa brujula te indica que estás mirando al {d[self.player.direction]}.'
        t += f'\n\tQuedan {self.player.arrows} {f} en el carcaj'
        print(t)
        perception_list = self.board[self.player.position]
        for perception in perception_list:
            print(self.codex[perception])
        return self

    # Fase 1 turno
    def do_action(self):
        """Estas son tus opciones:\n\t1- Avanzar\n\t2- Girar\n\t3- Atacar\n\t4- Escapar"""
        if self.action == 1:  # Avanzar
            self.one_step()
            print('Avanzas unos pasos y miras a tu alrededor')
            '''Wumpus -> 0, Oro -> 2, hoyos -> 4'''
            if 0 in self.board[self.player.position] and not self.death_wumpus:
                print('¡Te topas con el Wumpus y te ataca de frente! GAME OVER')
                self.config.endgame = True
                pass
            elif 2 in self.board[self.player.position] and not self.gold:
                print('¡FELICIDADES! ¡Has encontrado el tesoro del Wumpus!')
                self.gold = True
                self.codex[6] = 'Estás en la puerta de Entrada, ahora puedes huir'
                pass
            elif 4 in self.board[self.player.position]:
                print('¡En cuanto pones un pie en la oscuridad caes a un pozo sin fondo! GAME OVER')
                self.config.endgame = True
                pass

        if self.action == 2:  # Si Giras
            print('¿Hacia dónde te giras?\n\t1- Izquierda\n\t2- Derecha')
            turn_a = get_input_number()
            while not 1 <= turn_a <= 2:
                print('¡No puedo hacer nada con eso!')
                print('¿Hacia dónde te giras?\n\t1- Izquierda\n\t2- Derecha')
                turn_a = get_input_number()
            # Directions: 0 arriba, 1 izquierda, 2 derecha, 3 abajo
            # Turn_around: 1 izquierda 2 derecha
            if self.player.direction == 0:
                self.player.direction = 1 if turn_a == 1 else 2
            elif self.player.direction == 1:
                self.player.direction = 3 if turn_a == 1 else 0
            elif self.player.direction == 2:
                self.player.direction = 0 if turn_a == 1 else 3
            elif self.player.direction == 3:
                self.player.direction = 2 if turn_a == 1 else 1
            else:
                raise Exception('Error, self.player.direction fuera de rango de parámetros (0 a 3)')
        if self.action == 3:  # Si Atacas
            if self.player.arrows > 0:
                self.player.arrows = self.player.arrows - 1
                if self.wumpus_position in self.arrow_line():
                    print('¡¡ssszzzchump!! ¡Le diste al Wumpus! Escuchas un aullido que se va atenuando')
                    # ahora de verdad XD
                    self.death_wumpus = True
                    self.codex[0] = 'El cuerpo del Wumpus yace en el suelo'
                    self.codex[1] = 'El Wumpus ya no está, pero su hedor permanece...'

                else:
                    print('¡¡Clack!! ¡La flecha ha golpeado la pared! Cuidado, no tenemos muchas flechas')
            else:
                print('¡No te quedan flechas!')
        if self.action == 4:  # Si Escapas
            if self.gold and 6 in self.board[self.player.position]:
                self.config.endgame = True
                if self.death_wumpus:
                    print('¡FELICIDADES! ¡HAS GANADO EL JUEGO ACABANDO CON EL WUMPUS!')
                else:
                    print('¡FELICIDADES! ¡HAS GANADO EL JUEGO SALVANDO AL WUMPUS!')
            if not self.gold:
                print('No puedes escapar si no tienes el Tesoro')
            if 6 not in self.board[self.player.position]:
                print('No puedes escapar si no estás en la salida')
        return self

    def one_step(self):
        """0 arriba, 1 izquierda, 2 derecha, 3 abajo"""
        if self.player.direction == 0 and self.player.player_adj[0]:
            self.player.position = self.player.player_adj[0]
        elif self.player.direction == 1 and self.player.player_adj[1]:
            self.player.position = self.player.player_adj[1]
        elif self.player.direction == 2 and self.player.player_adj[2]:
            self.player.position = self.player.player_adj[2]
        elif self.player.direction == 3 and self.player.player_adj[3]:
            self.player.position = self.player.player_adj[3]
        else:
            print('¡Has tropezado con un muro!')
        self.player.player_adj = self.board.get_adjacents(self.player.position)
        return self

    def fill_board(self):
        """Rellena el tablero en base a esta Leyenda:
            Wumpus -> 0,
            Hedor adyacente -> 1,
            Oro -> 2,
            Brillo adyacente -> 3
            n-2 hoyos -> 4,
            Brisa adyacente -> 5,
            Entrada -> 6,
            Pared = 7 """
        free_cells = [n for n in range(self.config.board_size * self.config.board_size)]

        # PUERTA
        self.board.insert_in_board(6, self.player.position)  # PUERTA
        free_cells.remove(self.player.position)

        # WUMPUS
        pos = random.choice(free_cells)
        self.board.insert_in_board(0, pos)  # wumpus
        self.wumpus_position = pos
        free_cells.remove(pos)
        for n in self.board.adjacent_dict[pos]:
            self.board.insert_in_board(1, n)  # hedor

        # ORO
        pos = random.choice(free_cells)
        self.board.insert_in_board(2, pos)  # oro
        free_cells.remove(pos)
        for n in self.board.adjacent_dict[pos]:
            self.board.insert_in_board(3, n)  # brillo

        # HOYOS
        for _ in range(self.config.holes):
            pos = random.choice(free_cells)
            self.board.insert_in_board(4, pos)  # hoyo
            free_cells.remove(pos)
            for n in self.board.adjacent_dict[pos]:
                self.board.insert_in_board(5, n)  # brisa

        return self

    def arrow_line(self):
        """sabiendo la dirección y la posición del jugador calcula la trayectoria de una flecha
        (if e := f(): x= e es el nuevo 'walrus operator' de Python 3.8 https://docs.python.org/3.9/whatsnew/3.8.html)"""
        trajectory = []
        position = self.player.position
        if self.player.direction == 0:  # arriba
            while position:
                if (position := self.board.top_adjacent(position)) is not None:
                    trajectory.append(position)

        elif self.player.direction == 1:  # izquierda
            while position:
                if (position := self.board.prev_adjacent(position)) is not None:
                    trajectory.append(position)

        elif self.player.direction == 2:  # derecha
            while position:
                if (position := self.board.next_adjacent(position)) is not None:
                    trajectory.append(position)

        elif self.player.direction == 3:  # abajo
            while position:
                if (position := self.board.bot_adjacent(position)) is not None:
                    trajectory.append(position)

        return trajectory


class Board:
    def __init__(self, config):
        self.board_size = check_and_fix(config.board_size, 3, v='tamaño del mapa')
        self.holes = check_and_fix(
            config.holes,
            self.board_size - 2,
            (self.board_size * self.board_size) - 3,
            v='pozos sin fondo')
        self.board = {key: [] for key in [n for n in range(self.board_size * self.board_size)]}
        self.adjacent_dict = self.get_adjacent_dict()

    def __getitem__(self, item):
        return self.board[item]

    def get_adjacent_dict(self):
        """crea un diccionario con los adyacentes de cada casilla sin especificar su direccion"""
        return {key: self.get_adjacent_list(key) for key in [n for n in range(self.board_size * self.board_size)]}

    def get_adjacent_list(self, x) -> list:
        """Recibe una casilla y el tamaño del tablero, devuelve las casillas adyacentes
        (if e := f(): x= e es el nuevo 'walrus operator' de Python 3.8 https://docs.python.org/3.9/whatsnew/3.8.html)"""
        a = []
        if (e := self.prev_adjacent(x)) is not None:  # adyacente anterior
            a.append(e)
        if (e := self.next_adjacent(x)) is not None:  # adyacente posterior
            a.append(e)
        if (e := self.top_adjacent(x)) is not None:  # adyacente superior
            a.append(e)
        if (e := self.bot_adjacent(x)) is not None:  # adyacente inferior
            a.append(e)
        return a

    def get_ring(self):
        """devuelve las casillas del anillo exterior del tablero"""
        return [k for k, v in self.adjacent_dict.items() if len(v) < 4]

    def insert_in_board(self, elem, pos):
        """inserta un elemento <elem> en una casilla <pos> del tablero"""
        if elem not in self.board[pos]:
            self.board[pos].append(elem)
        return self

    def get_adjacents(self, x):
        """0 arriba, 1 izquierda, 2 derecha, 3 abajo"""
        return {
            0: self.top_adjacent(x),
            1: self.prev_adjacent(x),
            2: self.next_adjacent(x),
            3: self.bot_adjacent(x)}

    def prev_adjacent(self, x):
        """devuelve adyacente anterior a entrada o None"""
        return x - 1 \
            if x % self.board_size != 0 and x - 1 >= 0 else None

    def next_adjacent(self, x):
        """devuelve adyacente siguiente o None"""
        return x + 1 \
            if x % self.board_size != self.board_size - 1 and x + 1 <= (self.board_size * self.board_size) - 1 else None

    def top_adjacent(self, x):
        """devuelve adyacente superior o None"""
        return x - self.board_size \
            if x - self.board_size >= 0 else None

    def bot_adjacent(self, x):
        """devuelve adyacente inferior o None"""
        return x + self.board_size \
            if x + self.board_size <= (self.board_size * self.board_size) - 1 else None

    def print_board(self):
        """método para desarrolladores: permite visualizar el mapa"""
        print('Active Cheat: "black sheep wall"')
        d = {0: 'Wumpus', 1: 'Hedor', 2: 'Oro', 3: 'Brillo',
             4: 'Hoyo', 5: 'Brisa', 6: 'Entrada', 7: 'Pared', '[]': 'Vacio'}
        p = ''
        p2 = ''
        i = 0
        for n in self.board:
            un = 0
            ul = 0
            for c in self.board[n]:
                p += str(c) + ' '
                un += 2
                p2 += d[c] + ' '
                ul += len(d[c]) + 1
            i += 1
            p += (30 - un) * ' '
            p2 += (30 - ul) * ' '
            if i == self.board_size:
                i = 0
                p += '\n'
                p2 += '\n'

        print(p)
        print(p2)
        return self


class Player:
    def __init__(self, config, board):
        self.position = random.choice(board.get_ring())  # posicion del jugador en el tablero
        self.arrows = check_and_fix(config.arrows, 1, v='flechas')
        self.player_adj = board.get_adjacents(self.position)
        self.direction = random.randint(0, 3)


class Configuration:
    def __init__(self, board_size, holes, arrows):
        self.board_size = board_size
        self.holes = holes
        self.arrows = arrows
        self.endgame = None


def get_input_number():
    """devuelve el input del usuario siempre que este sea un numero"""
    i = None
    try:
        i = int(input('> '))
        return i
    except ValueError:
        pass
    while not isinstance(i, int):
        try:
            print('Una voz resuena desde el interior de la caverna... "sólo lo posible es real"')
            i = int(input('> '))
        except ValueError:
            print('Tiembla el suelo, ¡algo hizo clock! Esto parece peligroso.')
    return i


def check_and_fix(i, minimum, maximum=None, v=None):
    """comprueba y repara según un valor mínimo y/o máximo"""
    if maximum:
        if minimum < i < maximum:
            return i
        else:
            print(f'El minimo de {v} es {str(minimum)} y el máximo {str(maximum)}')
            if v:
                print(f'{v} fuera de rango corregido a su minimo de {minimum}')
            return minimum
    elif i < minimum:
        print(f'El minimo es {minimum}')
        if v:
            print(f'{v} corregido a su mínimo de {minimum}')
        return minimum
    else:
        return i
