# fields are m x n arrays, -1 = unknown, 0-8 = exposed squares, 9 = bomb
# true = solved, false = not solved
MINE = 9
UNKNOWN = -1


def neighbors(row, col, m, n, radius=1):
    lst = []
    for i in range(max(row - radius, 0), min(row + radius + 1, m)):
        for j in range(max(col - radius, 0), min(col + radius + 1, n)):
            if i == row and j == col:
                continue
            lst.append((i, j))
    return lst


def generate_field(mine_locations, m, n):
    field = [[0 for _ in range(n)] for _ in range(m)]
    for mine in mine_locations:
        row = mine[0]
        col = mine[1]
        field[row][col] = MINE
        for n_row, n_col in neighbors(row, col, m, n):
            if field[n_row][n_col] == 9:
                continue
            field[n_row][n_col] += 1
    return field


colors = {
    MINE: "\033[0;30;41m",  # red background
    1: "\033[34m",  # blue
    2: "\033[1;32;48m",
    3: "\033[31m",  # red
    4: "\033[1;31;48m",  # red
    5: "\033[1;31;48m",  # red
    6: "\033[1;30;48m",
    7: "\033[1;33;48m",
    8: "\033[1;33;48m",
    0: "\033[30m",  # black
    UNKNOWN: "\033[0;30;47m",  # blinking
    "END": "\033[0m",
}


def print_field(field):
    def color(item):
        return colors[item] + "{:3}".format(item) + colors["END"]

    print("\n".join(["".join([color(item) for item in row]) for row in field]))


def reveal(row, col, solution, field, m, n):
    if field[row][col] == MINE:
        print("You lost...")

    solution[row][col] = field[row][col]

    if solution[row][col] == 0:
        for n_row, n_col in neighbors(row, col, m, n):
            if solution[n_row][n_col] != UNKNOWN:
                continue
            reveal(n_row, n_col, solution, field, m, n)

    return solution


def flag(row, col, solution):
    solution[row][col] = MINE
    return solution


def next_step(solution, m, n):
    truth_matrix = [[False for _ in range(N)] for _ in range(M)]
    reveal = []
    reveal_all = []
    flags = []
    for i in range(m):
        for j in range(n):
            if solution[i][j] == UNKNOWN:
                continue
            if solution[i][j] == MINE:
                truth_matrix[i][j] = True
            mines = 0
            unknowns = []
            for n_row, n_col in neighbors(i, j, m, n):
                if solution[n_row][n_col] == MINE:
                    mines += 1
                if solution[n_row][n_col] == UNKNOWN:
                    unknowns.append((n_row, n_col))
            if mines == solution[i][j]:
                if len(unknowns) > 0:
                    reveal_all.append((i, j))
                else:
                    truth_matrix[i][j] = True
            elif mines + len(unknowns) == solution[i][j]:
                flags += unknowns

    return reveal_all, flags


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


def solve(field, row, col):
    print("\nStarting guess at ({0},{1})...".format(row, col))
    sol = [[-1 for _ in range(N)] for _ in range(M)]
    reveal(0, 0, sol, field, M, N)
    print_field(sol)
    while True:
        reveal_all, flags = next_step(sol, M, N)
        if not len(reveal_all) and not len(flags):
            break
        for i, j in flags:
            flag(i, j, sol)
        print("\nFlagging field...")
        print_field(sol)
        for i, j in reveal_all:
            for n_row, n_col in neighbors(i, j, M, N):
                if sol[n_row][n_col] == UNKNOWN:
                    reveal(n_row, n_col, sol, field, M, N)
        print("\nRevealing tiles...")
        print_field(sol)


print("Field1...")
field1 = generate_field(mines1, M, N)
print_field(field1)

solve(field1, 0, 0)
