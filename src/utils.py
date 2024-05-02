import csv
import json
import logging
import os
import sys
import time
from pathlib import Path
import random
from selenium.webdriver.common.keys import Keys
import string
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from datetime import datetime
import urllib
import json

handlers = [logging.FileHandler('error.log'), logging.StreamHandler()]

logging.basicConfig(handlers=handlers, level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
daily_count = 0
date_today = None


def btn_click(driver, xpath):
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))

    element.click()


def find_element(driver, by, sec, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, sec)))
    return element


def find_elements(driver, by, sec):
    return list(driver.find_elements(by, sec))


def insert_value(driver, xpath, text, previouse_clear=False):
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    if previouse_clear:
        element.clear()

    element.send_keys(text)


def insert_value_and_press_enter(driver, xpath, text, previouse_clear=False):
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    if previouse_clear:
        element.clear()

    element.send_keys(text)
    element.send_keys(Keys.ENTER)


def execute_script_based_click(driver, xpath, timeout=60):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", el)
    except Exception as ex:
        print(f'Error while clicking...{ex}')


def get_input_value(driver, xpath):
    return driver.find_element(By.XPATH, xpath).get_attribute('value')


def scroll_to_element_smoothly(driver, xpath):
    element = find_element(driver, By.XPATH, xpath)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'})",
                          element)


def index_click(driver, xpath, index):
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))


def get_element_text(driver, xpath):
    el = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    return el.text


def verify_element_enable(driver, xpath):
    try:
        el = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        return el.is_enabled()
    except:
        return False


def verify_element_disabled(driver, xpath):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    return element.is_disabled()


def get_normal_driver(headless=False, dir=None, isFullPath=False, add_extension=False, cloudwatch=None, cloudwatch_log_group_name=None):
    try:
        options = webdriver.ChromeOptions()
        if not add_extension:
            options.add_argument('--incognito')
        if dir is not None:
            path = f"{BASE_DIR}/{dir}"
        if isFullPath:
            path = dir
            options.add_argument(f"--user-data-dir={path}")
        options.add_argument("--log-level=3")
        options.add_argument('--no-sandbox')

        if headless:
            options.add_argument('--headless')
        if add_extension:
            # extension_path = f"{BASE_DIR}/anticaptcha-plugin_v0.63.zip"
            extension_path = os.path.join(os.getcwd(), "anticaptcha-plugin_v0.63.zip")
            options.add_extension(extension_path)
        options.add_argument('--start-maximized')
        chrome_exe_path = ChromeDriverManager().install()
        driver = webdriver.Chrome(service=Service(executable_path=chrome_exe_path), options=options)
        time.sleep(2)
        if add_extension:
            setup_anti_captcha_extension(driver, cloudwatch, cloudwatch_log_group_name)
        # setup_captcha_extension(driver)
        ManageChromeDriverCache(driver, os.path.abspath(__file__))
        return driver
    except Exception as e:
        print(e)
        if cloudwatch:
            try:
                error = {'log_group_name': cloudwatch_log_group_name,
                         'error': f"Exception while creating the new driver \n {traceback.print_exc()}"}
                log_to_cloudwatch(cloudwatch, **error)
            except:
                pass
        get_normal_driver(headless, add_extension=add_extension)