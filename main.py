# import module
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.minesweeperonline.com")
time.sleep(10)

# Obtain button by link text and click.
button = driver.find_element_by_link_text("Sign In")
button.click()
