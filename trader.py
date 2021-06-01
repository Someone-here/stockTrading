from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

options = Options()
Options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
Options.add_argument(options, "--headless")
Options.add_argument(options, "--disable-gpu")
Options.add_argument("--disable-dev-shm-usage")
Options.add_argument("--no-sandbox")
Options.add_argument(options, "--silent")

driver = webdriver.Chrome(executable_path=os.environ.get(
    "CHROMEDRIVER_PATH"), chrome_options=Options)


def setup(stock):
    driver.get(f"https://tradingview.com/symbols/{stock}")


def quote():
    return float(driver.find_element_by_css_selector("div.tv-symbol-price-quote__value.js-symbol-last").text)
