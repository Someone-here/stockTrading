from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

options = Options()
Options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
Options.add_argument(options, "--headless")
Options.add_argument(options, "--disable-gpu")
Options.add_argument(options, "--disable-dev-shm-usage")
Options.add_argument(options, "--no-sandbox")
Options.add_argument(options, "--silent")

driver = webdriver.Chrome(chrome_options=options)


def setup(stock: str):
    driver.get(f"https://tradingview.com/symbols/{stock}")


def quote():
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tv-symbol-price-quote__value.js-symbol-last"))
    )
    return float(element.text)
