import sys
import time

#  constants
MINE = 9
UNKNOWN = -1


class Array:
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
        UNKNOWN: "\033[0;30;47m",  # bold
        "END": "\033[0m",
    }

    def __init__(self, m, n, val):
        self.m = m
        self.n = n
        self.arr = [[val for _ in range(n)] for _ in range(m)]

    def __getitem__(self, item):
        return self.arr[item]

    def print(self):
        def color(item):
            return self.colors[item] + "{:3}".format(item) + self.colors["END"]

        def gray_block():
            return self.colors[UNKNOWN] + " " * 3 + self.colors["END"]

        print(gray_block() * (self.m + 2))
        print(
            ("\n").join(
                [
                    (
                        gray_block()
                        + "".join([color(item) for item in row])
                        + gray_block()
                    )
                    for row in self.arr
                ]
            )
        )
        print(gray_block() * (self.m + 2))

    def unprint(self):
        for _ in range(self.m + 2):
            sys.stdout.write("\x1b[1A")
            sys.stdout.write("\x1b[2K")

    def neighbors(self, i, j, radius=1):
        lst = set()
        for ii in range(max(i - radius, 0), min(i + radius + 1, self.m)):
            for jj in range(max(j - radius, 0), min(j + radius + 1, self.n)):
                if ii == i and jj == j:
                    continue
                lst.add((ii, jj))
        return lst

    def neighbors_mutual(self, locs, radius=1):
        assert(len(locs) == 2)
        inter = self.neighbors(locs[0][0], locs[0][1], radius).intersection(self.neighbors(locs[1][0], locs[1][1], radius))
        return inter

class Field(Array):
    def __init__(self, m, n):
        super().__init__(m, n, 0)
        self.field = self.arr

    def set_mines(self, mine_locations):
        for mine in mine_locations:
            i = mine[0]
            j = mine[1]
            self.field[i][j] = MINE
            for ni, nj in self.neighbors(i, j):
                if self.field[ni][nj] == 9:
                    continue
                self.field[ni][nj] += 1
        return self.field

class Solution(Array):
    def __init__(self, m, n):
        super().__init__(m, n, -1)
        self.solution = self.arr

    def set_flag(self, i, j):
        self.solution[i][j] = MINE

    def set_flags(self, flags):
        for i, j in flags:
            self.set_flag(i, j)

    def next_step(self):
        reveal_all = set()
        reveal = set()
        flags = set()
        unknown_neighbor = {}
        mine_neighbor = {}
        for i in range(self.m):
            for j in range(self.n):
                if self.solution[i][j] == UNKNOWN:
                    continue
                elif self.solution[i][j] == MINE:
                    continue
                mines = 0
                unknowns = set()
                solution_val = self.solution[i][j]
                for ni, nj in self.neighbors(i, j):
                    if self.solution[ni][nj] == MINE:
                        mines += 1
                    elif self.solution[ni][nj] == UNKNOWN:
                        unknowns.add((ni, nj))
                unknown_neighbor[(i, j)] = unknowns
                mine_neighbor[(i, j)] = mines

                if mines == solution_val:
                    if len(unknowns) > 0:
                        reveal_all.add((i, j))
                elif mines + len(unknowns) == solution_val:
                    flags.update(unknowns)

        for i, j in unknown_neighbor.keys():
            solution_val = self.solution[i][j]
            if solution_val == MINE or solution_val == UNKNOWN:
                continue
            elif (
                solution_val - mine_neighbor[(i, j)] == 1 # remaining mines 1
                and len(unknown_neighbor[(i, j)]) == 2 # unknowns 2
            ):
                neighbors = unknown_neighbor[(i, j)]
                mutuals = self.neighbors_mutual(list(neighbors))
                for mi, mj in mutuals:
                    if not (mi, mj) in unknown_neighbor:
                        continue
                    if unknown_neighbor[(mi, mj)].issuperset(neighbors):
                        remaining_mines = self.solution[mi][mj] - mine_neighbor[(mi, mj)]
                        remaining_neighbors = unknown_neighbor[((mi, mj))] ^ neighbors
                        if remaining_mines == 1:
                            reveal.update(remaining_neighbors)
                        elif remaining_mines - 1 == len(remaining_neighbors):
                            flags.update(remaining_neighbors)
                
        return reveal_all, flags, reveal


class Game:
    def __init__(self, field, solution):
        assert isinstance(field, Field)
        assert isinstance(solution, Solution)
        self.field = field
        self.solution = solution

    def reveal(self, i, j):
        if self.field.field[i][j] == MINE:
            print("You lost...")

        self.solution[i][j] = self.field[i][j]

        if self.solution[i][j] == 0:
            for ni, nj in self.solution.neighbors(i, j):
                if self.solution[ni][nj] != UNKNOWN:
                    continue
                self.reveal(ni, nj)

    def solve(self, i=0, j=0):
        print("Starting guess at ({0},{1})...".format(i, j))
        self.reveal(i, j)
        self.solution.print()
        while True:
            reveal_all, flags, reveal = self.solution.next_step()
            if not len(reveal_all) and not len(flags):
                break
            self.solution.unprint()
            for i, j in flags:
                self.solution.set_flag(i, j)
            print("Flagging field...")
            for i, j in reveal_all:
                for ni, nj in self.solution.neighbors(i, j):
                    if self.solution[ni][nj] == UNKNOWN:
                        self.reveal(ni, nj)
            for i, j in reveal:
                self.reveal(i, j)
            print("Revealing tiles...")
            self.solution.print()
            time.sleep(0.5)
