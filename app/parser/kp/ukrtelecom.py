import conf

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

from parser.parser import DinamicParser
from parser.tools import clear_text

delay = 8

class Ukrtelecom(DinamicParser):

    def __init__(self, **kwargs):
        super( Ukrtelecom, self ).__init__(**kwargs)
        self.__tarifs = []
        self.__param = kwargs

    def get_coordinates(self):
        return self.__param['coordinates']

    def parse(self, region_id, area_id, locality_id):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')        
        browser = webdriver.Chrome(chrome_options=options, executable_path=conf.PATH_TO_CHROMEDRIVER)
        browser.get(self.get_url())

        sleep(delay)
        loc = browser.find_element_by_xpath('//div[@class="current-location__location"]').click()
        sleep(delay)
        reg = browser.find_element_by_xpath(f'//a[@data-id="{region_id}"]').click()
        sleep(delay)
        reg = browser.find_element_by_xpath(f'//a[@data-id="{area_id}"]').click()
        sleep(delay)
        reg = browser.find_element_by_xpath(f'//a[@data-id="{locality_id}"]').click()

        generated_html = browser.page_source
        browser.quit()
        return bs(generated_html, 'lxml')

def trf_parser(**params):

    parser = Ukrtelecom(
        name='ukrtelecom',
        url='https://new.ukrtelecom.ua/internet/',
        coordinates=params['coordinates'])

    coordinates = parser.get_coordinates()
    region_id = coordinates[0]
    area_id = coordinates[1]
    locality_id = coordinates[2]
    locality_name = coordinates[3]

    competitor = f'{parser.get_name()}-{locality_name}'
    parser.set_name(competitor)

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse(region_id, area_id, locality_id)

    tarifs = soup.find_all('section', attrs='card_price')

    for tarif in tarifs:
        title = tarif.find('h3', attrs='card__header').text
        title_sub = tarif.find('div', attrs='card__sub-header').text
        title = clear_text(title,['strip', 'line breaks', 'specials'])
        title_sub = clear_text(title_sub,['strip', 'line breaks', 'specials'])
        title += f' {title_sub}'

        price = tarif.find('div', attrs='price-tag__current-price').text
        price = clear_text(price,['full'])
        price += 'грн/мес'

        if title and price:
            tarif_dic = {'title':title, 'price':price}
        all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser