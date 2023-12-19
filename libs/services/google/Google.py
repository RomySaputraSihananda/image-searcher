from selenium import webdriver;
from selenium.webdriver.chrome.options import Options;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support import expected_conditions as EC;

options: Options = Options();
options.add_argument('--headless');

class Google:
    def __init__(self) -> None:        
        self.__browser: webdriver = webdriver.Chrome(options=options);