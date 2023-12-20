from selenium import webdriver;
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from pyquery import PyQuery
from json import dumps

from libs.helpers import Parser

options: Options = Options()
options.add_argument('--headless')

class Google:
    def __init__(self) -> None:        
        self.__driver: WebDriver = webdriver.Chrome(options=options)
        self.__driver.set_window_size(1920, 1080)
        self.__parser: Parser = Parser()

        self.__result: dict = {}
        # self.__result

    def __wait_element(self, selector: str, timeout=10):
        return WebDriverWait(self.__driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def __filter_image(self, container: PyQuery) -> None:
        for div in container('.G19kAf.ENn9pd'):
            data: PyQuery = self.__parser.execute(div, '.ksQYvb')

            self.__result['data'].append({
                "source": data.attr('data-action-url').split('/')[2],
                "url_image": data.attr('data-thumbnail-url'),
                "url_website": data.attr('data-action-url'),
                "url_website_icon": self.__parser.execute(div, '.PlAMyb img').attr('src') if not self.__parser.execute(div, '.PlAMyb img').attr('data-src') else self.__parser.execute(div, '.PlAMyb img').attr('data-src'),
                "caption": data.attr('data-item-title')
            })

    def search_image(self, path: str) -> dict:
        self.__result['data'] = []

        self.__driver.get('https://google.com')
        
        self.__wait_element('.nDcEnd').click()
        self.__wait_element('input[type=file]:nth-child(1)').send_keys(path)
        self.__wait_element('.aah4tc')

        container: PyQuery = self.__parser.execute(self.__driver.page_source, '.aah4tc')

        self.__driver.close()

        self.__filter_image(container)

        return self.__result
    
    def search_image_by_url(self, url_image: str) -> dict:
        self.__result['data'] = []

        self.__driver.get(f'https://lens.google.com/uploadbyurl?url={url_image}')

        container: PyQuery = self.__parser.execute(self.__driver.page_source, '.aah4tc')

        self.__driver.close()

        self.__filter_image(container)

        return self.__result

# testing
if(__name__ == '__main__'):
    google: Google = Google()
    data: dict = google.search_image_by_url('http://45.146.106.80:9595/assets/img/') 
    
    with open('test_data.json', 'w') as file:
        file.write(dumps(data, indent=2, ensure_ascii=False))

    # import undetected_chromedriver as uc
    # driver = uc.Chrome(headless=True,use_subprocess=False)
    # driver.get('https://nowsecure.nl')
    # driver.save_screenshot('nowsecure.png')