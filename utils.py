import re
import os
import time
import logging
from shutil import rmtree
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime


def create_driver() -> webdriver.Chrome:
    path = ChromeDriverManager().install()
    service = Service(path)
    options = Options()
    options.add_argument("--headless")  # Hides the browser window.
    options.add_argument("--no-sandbox")  # Bypass OS security model.
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems.
    options.add_argument('log-level=3')  # Suppress console logs.
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def create_local_web_page(url, path):
    driver = create_driver()
    try:
        driver.get(url)
        time.sleep(5)
        html_content = driver.page_source
        with open(path, 'w', encoding='utf-8') as file:
            file.write(html_content)
            logging.info(f"Saved HTML content to file: {path}")
    except Exception as e:
        logging.error(f"Error while saving HTML content: {e}")
    finally:
        driver.quit()

def create_web_page_soup(url):
    invalid_chars = r'[&-_+.=<>:"/\\|?*]'
    sanitized_name = re.sub(invalid_chars, '', url)
    dir_path = f'tmp_website_{datetime.now().strftime("%Y_%m_%d")}'
    
    # Cleanup old temporary directories
    for folder in os.listdir():
        if folder.startswith('tmp_website') and folder != dir_path:
            rmtree(folder)
    
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    
    path = os.path.join(dir_path, sanitized_name + '.html')
    html_content = None
    
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            logging.info(f"Loaded HTML content from file: {path}")
    else:
        create_local_web_page(url, path)
        with open(path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    if not soup.find_all('a'):
        os.remove(path)
        create_local_web_page(url, path)
        with open(path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
    
    return soup
