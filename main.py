import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import argparse

from minesweeper import *

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", default="beginner")

args = parser.parse_args()
mode = args.mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver = webdriver.Safari()

driver.get("https://www.minesweeperonline.com/#{0}".format(mode))
time.sleep(2)

classes = {
    "square blank": UNKNOWN,
    "square open0": 0,
    "square open1": 1,
    "square open2": 2,
    "square open3": 3,
    "square open4": 4,
    "square open5": 5,
    "square open6": 6,
    "square open7": 7,
    "square open8": 8,
    "square bombflagged": MINE,
}


modes = {
    "beginner": (9, 9, 10),
    "intermediate": (16, 16, 40),
    "expert": (16, 30, 99)
}
M, N, F = modes[mode]


def process_grid(driver, m, n):
    grid = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            grid[i][j] = driver.find_element(By.ID, "{0}_{1}".format(i + 1, j + 1))
    return grid


def grid_to_array(array, grid, m, n):
    for i in range(m):
        for j in range(n):
            if array[i][j] != UNKNOWN:
                continue
            array[i][j] = classes[grid[i][j].get_attribute("class")]


grid = process_grid(driver, M, N)
solution = Solution(M, N)

action = ActionChains(driver, 0)

face = driver.find_element(By.ID, "face")
def remaining_unknown(grid):
    unknown_remaining = 0
    for row in grid:
        for tile in row:
            if tile == UNKNOWN:
                unknown_remaining += 1
    return unknown_remaining

def play(i=0, j=0):
    grid[i][j].click()
    grid_to_array(solution.solution, grid, M, N)
    while True:
        grid_to_array(solution.solution, grid, M, N)
        reveal_all, flags, reveal = solution.next_step()
        if not len(reveal_all) and not len(flags):
            break
        for i, j in flags:
            solution.set_flag(i, j)
        for i, j in reveal_all:
            for ni, nj in solution.neighbors(i, j):
                if solution[ni][nj] == UNKNOWN:
                    grid[ni][nj].click()
        for i, j in reveal:
            grid[i][j].click()
    return False

wins = 0
losses = 0
while True:
    try:
        play(2,2)
        losses +=1
        solution.print()
    except:
        wins += 1
        # alert = driver.switch_to.alert
        # alert.accept()

    print("Wins: {0} Losses: {1} Win Rate: {2}".format(wins, losses, wins/ (wins + losses)))
    solution = Solution(M, N)
    time.sleep(2)
    face.click()
