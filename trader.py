from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    driver.implicitly_wait(0.01)
    return float(driver.find_element_by_css_selector("div.tv-symbol-price-quote__value.js-symbol-last").text)
