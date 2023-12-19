from selenium import webdriver;
from selenium.webdriver.chrome.options import Options;
from selenium.webdriver.chrome.service import Service;

from time import sleep
from pyquery import PyQuery
from json import dumps

import requests

from libs.helpers import Parser

options: Options = Options();
options.add_argument('--headless');

class Google:
    def __init__(self) -> None:        
        self.__driver: webdriver = webdriver.Chrome(service=Service(executable_path='./chromedriver'));
        self.__parser: Parser = Parser()

        self.__result: dict = {}
    
    def __wait_element(self, selector: str) -> any:
        while True:
            try:
                return self.__driver.find_element("css selector", selector)
            except Exception:
                pass

    def __filter_image(self, container: PyQuery) -> None:
        for div in container('.G19kAf.ENn9pd'):

            self.__result['data'].append({
                "url_image": self.__parser.execute(div, '.Me0cf img').attr('src') if not self.__parser.execute(div, '.Me0cf img').attr('data-src') else self.__parser.execute(div, '.Me0cf img').attr('data-src'),
                "url_icon_website": self.__parser.execute(div, '.PlAMyb img').attr('src') if not self.__parser.execute(div, '.PlAMyb img').attr('data-src') else self.__parser.execute(div, '.PlAMyb img').attr('data-src'),
            })
            

    def start(self, path: str) -> dict:
        self.__result['data'] = []

        self.__driver.get('https://google.com')

        self.__wait_element('.nDcEnd .Gdd5U').click()
        self.__wait_element('input[type=file]:nth-child(1)').send_keys(path)
        self.__wait_element('.aah4tc')

        container: PyQuery = self.__parser.execute(self.__driver.page_source, '.aah4tc')
        self.__driver.close()

        self.__filter_image(container)

        return self.__result



# testing
if(__name__ == '__main__'):
    google: Google = Google()
    data: dict = google.start('/home/romy/Destop/data-sensor/image-searcher/test.jpg') 
    
    with open('test_data.json', 'w') as file:
        file.write(dumps(data, indent=2, ensure_ascii=False))
    
    for i, img in enumerate(data['data']):
        with open(f'test/img/{i}.jpg', 'wb') as file:
            file.write(requests.get(img['url_image']).content)

        with open(f'test/icon/{i}.jpg', 'wb') as file:
            file.write(requests.get(img['url_icon_website']).content)

    # import undetected_chromedriver as uc
    # driver = uc.Chrome(headless=True,use_subprocess=False)
    # driver.get('https://nowsecure.nl')
    # driver.save_screenshot('nowsecure.png')