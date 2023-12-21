
from pyquery import PyQuery
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from libs.helpers import Parser
from libs.helpers import Datetime


class Bing:
    def __init__(self):

        self.__parser = Parser()
        self.__time = Datetime()
        self.__base_url = 'https://www.bing.com/'
        self.__image_url = 'https://www.bing.com/images/search'

    
    def __url_complement(self, url):
        if self.__image_url not in url:
            return self.__image_url+url
        return url 


    def __component(self, text: str):
        comp = []
        try:
            comp.append(text.split(' ')[0])
            comp.append(text.split(' ')[2])
            comp.append(text.split(' ')[4])
        except IndexError:
            comp.append(' ')
            comp.append(' ')
            comp.append(' ')
        finally:
            return comp


    def __retry(self, url, max_retries= 5, retry_interval= 0.2) -> webdriver :
        for _ in range(max_retries):
            options = Options()
            options.add_argument('--headless=new')
            driver = webdriver.Chrome(options=options)

            try:
                driver.set_page_load_timeout(15)
                driver.get(url=url)
                return driver
            except Exception as err:
                driver.close()

            sleep(retry_interval)
            retry_interval+= 0.2
        return driver

    def __search(self, driver):
        results = {
            "time": self.__time.now(),
            "search_result": [],
            "related_searches": [],
            "total_search": 0,
            "total_related": 0
        }

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="detailCanvas"]/div[2]/div/div[1]/div/ul/li/span/span[2]')))
            if self.__parser.execute(source=driver.page_source, selector='#detailCanvas > div:nth-of-type(2) > div > div:first-of-type > div > ul > li > span > span:nth-of-type(2)')[-1].text == 'No results': return results
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'vs_images')))
        except TimeoutException as err:
            raise err

        last = None
        while True:

            driver.execute_script("window.scrollTo(0, document.querySelector('.expander_container ul').scrollHeight);")
            sleep(1)
            new_height = driver.execute_script("return document.querySelector('.expander_container ul').scrollHeight")
            if last == new_height: break 
            last = new_height
        
        table: PyQuery = self.__parser.execute(source=driver.page_source, selector='#vs_images > div > div > ul')

        search_result = [li for li in table.find('li') if self.__parser.execute(source=li, selector='div:first-child div:first-child div:first-child a').attr('href') is not None]
        related_searches = [li for li in table.find('div.irsc div.irsb div.irsuc')]

        results['total_search'] = len(search_result)
        results['total_related'] = len(related_searches)
        results['search_result'] = [{
            'url_image': self.__url_complement(self.__parser.execute(source=li, selector='div:first-child div:first-child div:first-child a').attr('href')),
            'url_thumb': self.__parser.execute(source=li, selector='div:first-child div:first-child div:first-child a img').attr('src'),
            'descriptions': self.__parser.execute(source=li, selector='div:first-child div:first-child div:first-child a img').attr('alt').split('detail. ')[-1],
            'width':  self.__component(self.__parser.execute(source=li, selector='div:first-child div:first-child div:first-child ul:first-child li:first-child span').text())[0],
            'height': self.__component(self.__parser.execute(source=li, selector='div:first-child div:first-child div:first-child ul:first-child li:first-child span').text())[1],
            'format': self.__component(self.__parser.execute(source=li, selector='div:first-child div:first-child div:first-child ul:first-child li:first-child span').text())[2],
        } for li in search_result]

        results['related_searches'] = [{
            'url_image': self.__url_complement(self.__parser.execute(source=li, selector='a').attr('href')),
            'url_thumb': self.__parser.execute(source=li, selector='img').attr('src'),
            'descriptions': self.__parser.execute(source=li, selector='img').attr('alt'),
        } for li in related_searches]

        driver.close()

        return results


    def search_by_url(self, url: str):
        print(url)
        try:
            driver = self.__retry(url=f'https://bing.com/images/search?view=detailv2&iss=sbi&form=SBIIDP&sbisrc=UrlPaste&q=imgurl:{url}')
            return self.__search(driver=driver)
        except Exception as err:
            raise err



    def search_by_image(self, image: str):

        driver = self.__retry(url=self.__base_url)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))).send_keys(image)
            return self.__search(driver=driver)
        except Exception as err:
            raise err

            
    
