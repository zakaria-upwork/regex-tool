import re
import os
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver 
from bs4 import BeautifulSoup
import time
from datetime import datetime
path = ChromeDriverManager().install()

def create_driver() -> webdriver.Chrome:
    service = Service(path)
    options = Options()
    options.add_argument("--headless") # Hides the browser window.
    options.add_argument("--no-sandbox")  # Bypass OS security model.
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems.
    options.add_argument('log-level=3') # Suppress console logs.
    driver = webdriver.Chrome(service=service, options=options)
    return driver
# from utils import create_driver
def create_local_web_page(url):
    invalid_chars = r'[&-_+.=<>:"/\\|?*]'
    sanitized_name = re.sub(invalid_chars, '', url)
    dir_path = f'tmp_website_{datetime.now().strftime("%Y_%m_%d")}'
    for folder in os.listdir():
        if folder.startswith('tmp_website') and folder != dir_path:
            os.rmdir(folder)
    if dir_path not in os.listdir():
        os.mkdir(dir_path)
    path = dir_path+'/' + sanitized_name + '.html'
    if os.path.exists(path):
        with open(path, 'r') as file:
            html_content = file.read()
    else:
        driver = create_driver()
        driver.get(url)
        time.sleep(5)
        html_content = driver.page_source
        with open(path, 'w') as file:
            file.write(html_content)
        driver.quit()
    soup = BeautifulSoup(html_content)
    return soup
