from selenium import webdriver;
from selenium.webdriver.chrome.options import Options;

from libs.helpers import Parser

# options: Options = Options();
# options.add_argument('--headless');

class Google:
    def __init__(self) -> None:        
        self.__browser: webdriver = webdriver.Chrome();
        self.__parser: Parser = Parser()
    


    def start(self) -> None:
        self.__browser.get('https://google.com')
        WebDriverWait(self.__browser, 10).until(EC.presence_of_element_located(By.CLASS_NAME, 'nDcEnd'))




if(__name__ == '__main__'):
    google: Google = Google()
    google.start() 