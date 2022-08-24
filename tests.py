from minesweeper import *

M = 9
N = 9
mines1 = [
    (0, 4),
    (0, 5),
    (0, 7),
    (2, 4),
    (5, 0),
    (5, 7),
    (6, 5),
    (6, 6),
    (7, 6),
    (8, 8),
]

mines2 = [
    (0, 0),
    (1, 4),
    (2, 3),
    (2, 8),
    (3, 2),
    (5, 2),
    (6, 2),
    (6, 8),
    (7, 3),
    (8, 5),
]

mines3 = [
    (4, 1),
    (4, 2),
    (4, 4),
    (5, 3),
    (5, 6),
    (5, 7),
    (6, 5),
    (7, 0),
    (7, 6),
    (8, 3),
]


def run_test(mines, m, n, initial_guess=(0, 0)):
    field = Field(m, n)
    field.set_mines(mines)
    print("Solution...")
    field.print()
    sol = Solution(m, n)
    game = Game(field, sol)
    game.solve(initial_guess[0], initial_guess[1])


run_test(mines1, M, N, (0, 0))
run_test(mines2, M, N, (4, 4))
run_test(mines3, M, N, (0, 0))
