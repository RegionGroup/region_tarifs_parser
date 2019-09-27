import conf

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

from parser.parser import DinamicParser
from parser.tools import clear_text

delay = 8

class Vodafone(DinamicParser):

    def __init__(self, **kwargs):
        super( Vodafone, self ).__init__(**kwargs)
        self.__tarifs = []
        self.__param = kwargs

    def parse(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')        
        browser = webdriver.Chrome(chrome_options=options, executable_path=conf.PATH_TO_CHROMEDRIVER)
        browser.get(self.get_url())
        sleep(20)
        generated_html = browser.page_source
        browser.quit()
        return bs(generated_html, 'lxml')

def trf_parser(**params):

    parser = Vodafone(
        name='Vodafone.ua',
        url='https://www.vodafone.ua/uk/privatnim-klientam/rates#inet')

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()
    divs = soup.find_all('div', attrs='bundle__summary')

    for div in divs:
        title = div.find('div', attrs='bundle-title').text
        title = clear_text(title, ['full'])
        price = div.find('strong', attrs='bundle-price__cost').text
        price = clear_text(price, ['full'])
        if "Unlim" in title: 
            if title and price:
                tarif_dic = {'title':title, 'price':price}
            all_tarifs.append(tarif_dic)

    all_tarifs = [dict(t) for t in {tuple(d.items()) for d in all_tarifs}]

    parser.set_tarifs(all_tarifs)
    return parser