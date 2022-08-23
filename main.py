# import module
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from minesweeper import *

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.minesweeperonline.com/#beginner")
time.sleep(5)

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

M = 9
N = 9

def process_grid(driver, m, n):
    grid = [[0 for _ in range(n)] for _  in range(m)]
    for i in range(m):
        for j in range(n):
            grid[i][j] = driver.find_element(By.ID, "{0}_{1}".format(i+1, j+1))
    return grid

def grid_to_array(array, grid, m, n):
    for i in range(m):
        for j in range(n):
            array[i][j] = classes[grid[i][j].get_attribute("class")]

grid = process_grid(driver, M, N)
solution = Solution(M,N)

action = ActionChains(driver, 0)

face = driver.find_element(By.ID, "face")

def play(i = 0, j = 0):
    print("Starting guess at ({0},{1})...".format(i, j))
    grid[i][j].click()
    time.sleep(0.5)
    while True:
        grid_to_array(solution.solution, grid, M, N)
        reveal_all, flags = solution.next_step()
        if not len(reveal_all) and not len(flags):
            break
        print("Flagging field...")
        for i, j in flags:
            solution.set_flag(i, j)
            action.context_click(grid[i][j]).perform()
        print("Revealing tiles...")       
        for i, j in reveal_all:
            for ni, nj in solution.neighbors(i, j):
                if solution[ni][nj] == UNKNOWN:
                    grid[ni][nj].click()
                    if face.get_attribute("class") == "facewin":
                        return
try:
    play(2,2)
except:
    pass
    # alert = driver.switchTo().alert()
    # alert.accept()

while True:
    time.sleep(5)
