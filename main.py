# import module
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# get https://www.geeksforgeeks.org
driver.get("https://www.minesweeperonline.com")

# Maximize the window and let code stall
# for 10s to properly maximise the window.
driver.maximize_window()
time.sleep(10)

# Obtain button by link text and click.
button = driver.find_element_by_link_text("Sign In")
button.click()
