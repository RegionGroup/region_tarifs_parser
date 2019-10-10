import requests
from bs4 import BeautifulSoup as bs
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import conf

# Заголовок для http-запросов
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.105 Safari/537.36 Viv/2.4.1488.38",
}


class Parser(object):
    def __init__(self, **kwargs):
        self.__tarifs = []
        self.__param = kwargs

    def get_name(self):
        return self.__param["name"]

    def get_url(self):
        return self.__param["url"]

    def get_locality(self):
        return self.__param["locality"]

    def get_cnct_type(self):
        return self.__param["cnct_type"]

    def get_habitation(self):
        return self.__param["habitation"]

    def get_tarifs(self):
        return self.__tarifs

    def set_name(self, name):
        self.__param["name"] = name

    def set_url(self, url):
        self.__param["url"] = url

    def set_tarifs(self, all_tarifs):
        self.__tarifs = all_tarifs

    def parse(self):

        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        try:
            request = session.get(self.get_url(), headers=headers)
        except:
            request = session.get(self.get_url(), headers=headers, verify=False)
        if request.status_code == 200:
            return bs(request.content, "lxml")


class DinamicParser(Parser):
    def parse(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        # options.add_argument('--enable-features=NetworkService')
        options.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(
            chrome_options=options, executable_path=conf.PATH_TO_CHROMEDRIVER
        )
        browser.get(self.get_url())
        generated_html = browser.page_source
        browser.quit()
        return bs(generated_html, "lxml")
