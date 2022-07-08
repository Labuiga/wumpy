import pytest
import wumpus_v1


@pytest.mark.parametrize(
    "int_a, int_b, int_c, str_a, expected",
    [
        (3, 3, None, "tamaño tablero", 3),
        (5, 3, None, "tamaño tablero", 5),
        (1, 3, None, "tamaño tablero", 3),
        (3, 1, 9, "pozos sin fondo", 3),
        (-1, 1, 9, "pozos sin fondo", 1),
        (25, 3, 9, "pozos sin fondo", 3),
    ]
)
def test_check_and_fix_multi(int_a, int_b, int_c, str_a, expected):
    assert wumpus_v1.check_and_fix(int_a, int_b, int_c, str_a) == expected


@pytest.mark.parametrize(
    "int_a, int_b, int_c, expected",
    [
        (3, 3, 3, "HuntTheWumpus"),
        (4, 2, 5, "HuntTheWumpus"),
        (25, 25, 25, "HuntTheWumpus"),
        (3, 100, 9, "HuntTheWumpus"),
        (-1, 1, 9, "HuntTheWumpus"),
        (4, -1, 9, "HuntTheWumpus"),
        (4, 2, -5, "HuntTheWumpus"),
    ]
)
def test_object(int_a, int_b, int_c, expected):
    w_object = wumpus_v1.HuntTheWumpus(int_a, int_b, int_c)
    assert type(w_object).__name__ == expected
    # errors = []
    # if type(w_object).__name__ != expected:
    #     errors.append("El objeto no es el esperado")
    # assert not errors, "errors occured:\n{}".format("\n".join(errors))


@pytest.mark.parametrize(
    "int_a, int_b, int_c, expected",
    [
        (3, 1, 10, 9),
        (4, 2, 10, 16),
        (5, 3, 10, 25),
        (6, 3, 10, 36),
        (7, 3, 10, 49),
        (8, 3, 10, 64),
        (9, 3, 10, 81),
    ]
)
def test_board_len(int_a, int_b, int_c, expected):
    w_object = wumpus_v1.HuntTheWumpus(int_a, int_b, int_c)
    assert len(w_object.board) == expected


@pytest.mark.parametrize(
    "int_a, int_b, int_c, expected",
    [
        (3, 3, 5, (9, 1, 1, 1, 3)),
        (4, 3, 5, (16, 1, 1, 1, 3)),
        (5, 5, 10, (25, 1, 1, 1, 5)),
    ]
)
def test_fill_board(int_a, int_b, int_c, expected):
    """Comprueba que el tablero se ha rellenado según los parámetros.
        Wumpus -> 0, Oro -> 2, hoyos -> 4, Entrada -> 6"""
    w_object = wumpus_v1.HuntTheWumpus(int_a, int_b, int_c).fill_board()
    cells = 0
    door = 0
    wump = 0
    gold = 0
    wells = 0
    for cell in w_object.board.values():
        cells += 1
        # print(str(cell))
        for e in cell:
            if e == 6:
                door += 1
            if e == 0:
                wump += 1
            if e == 2:
                gold += 1
            if e == 4:
                wells += 1
    # assert cells == expected[0] \
    #        and wells == expected[4] \
    #        and door == expected[1] \
    #        and wump == expected[2] \
    #        and gold == expected[3]
    assert (cells, door, wump, gold, wells) == expected


@pytest.mark.parametrize(
    "int_a, int_b, int_c, expected",
    [
        (3, 1, 10, {0: [1, 3], 1: [0, 2, 4], 2: [1, 5], 3: [4, 0, 6], 4: [3, 5, 1, 7], 5: [4, 2, 8], 6: [7, 3], 7: [6, 8, 4], 8: [7, 5]}),
        (4, 2, 10, {0: [1, 4], 1: [0, 2, 5], 2: [1, 3, 6], 3: [2, 7], 4: [5, 0, 8], 5: [4, 6, 1, 9], 6: [5, 7, 2, 10], 7: [6, 3, 11], 8: [9, 4, 12], 9: [8, 10, 5, 13], 10: [9, 11, 6, 14], 11: [10, 7, 15], 12: [13, 8], 13: [12, 14, 9], 14: [13, 15, 10], 15: [14, 11]}),
        (5, 3, 10, {0: [1, 5], 1: [0, 2, 6], 2: [1, 3, 7], 3: [2, 4, 8], 4: [3, 9], 5: [6, 0, 10], 6: [5, 7, 1, 11], 7: [6, 8, 2, 12], 8: [7, 9, 3, 13], 9: [8, 4, 14], 10: [11, 5, 15], 11: [10, 12, 6, 16], 12: [11, 13, 7, 17], 13: [12, 14, 8, 18], 14: [13, 9, 19], 15: [16, 10, 20], 16: [15, 17, 11, 21], 17: [16, 18, 12, 22], 18: [17, 19, 13, 23], 19: [18, 14, 24], 20: [21, 15], 21: [20, 22, 16], 22: [21, 23, 17], 23: [22, 24, 18], 24: [23, 19]}),
        (6, 3, 10, {0: [1, 6], 1: [0, 2, 7], 2: [1, 3, 8], 3: [2, 4, 9], 4: [3, 5, 10], 5: [4, 11], 6: [7, 0, 12], 7: [6, 8, 1, 13], 8: [7, 9, 2, 14], 9: [8, 10, 3, 15], 10: [9, 11, 4, 16], 11: [10, 5, 17], 12: [13, 6, 18], 13: [12, 14, 7, 19], 14: [13, 15, 8, 20], 15: [14, 16, 9, 21], 16: [15, 17, 10, 22], 17: [16, 11, 23], 18: [19, 12, 24], 19: [18, 20, 13, 25], 20: [19, 21, 14, 26], 21: [20, 22, 15, 27], 22: [21, 23, 16, 28], 23: [22, 17, 29], 24: [25, 18, 30], 25: [24, 26, 19, 31], 26: [25, 27, 20, 32], 27: [26, 28, 21, 33], 28: [27, 29, 22, 34], 29: [28, 23, 35], 30: [31, 24], 31: [30, 32, 25], 32: [31, 33, 26], 33: [32, 34, 27], 34: [33, 35, 28], 35: [34, 29]}),
    ]
)
def test_get_adjacent_dict(int_a, int_b, int_c, expected):
    adjacent_dict = wumpus_v1.HuntTheWumpus(int_a, int_b, int_c).get_adjacent_dict()
    assert adjacent_dict == expected