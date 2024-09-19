from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait



def get_web_element(driver: webdriver, expectation, xpath, timeout=5):
    try:
        el = WebDriverWait(driver, timeout).until(
            expectation((By.XPATH, xpath))
        )
        return el
    except NoSuchElementException as e:
        print(f"An error occurred: {e}")
        return None