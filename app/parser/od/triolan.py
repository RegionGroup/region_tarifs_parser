import conf

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

from parser.parser import DinamicParser
from parser.tools import clear_text

delay = 8

class Triolan(DinamicParser):

    def __init__(self, **kwargs):
        super( Triolan, self ).__init__(**kwargs)
        self.__tarifs = []
        self.__param = kwargs

    def parse(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')        
        browser = webdriver.Chrome(chrome_options=options, executable_path=conf.PATH_TO_CHROMEDRIVER)
        browser.get(self.get_url())
        pick = browser.find_element_by_xpath('//b[@class="trigger"]').click()
        sleep(delay)
        pick = browser.find_element_by_xpath('//li[@data="od"]').click()
        sleep(delay)
        generated_html = browser.page_source
        browser.quit()        
        return bs(generated_html, 'lxml')

def trf_parser(**params):

    parser = Triolan(
        name='Triolan',
        url='http://triolan.com/articles.aspx?k=connections&lng=ru&reg=od')

    tarif_dic = {}
    all_tarifs = []
    all_tarifs_tmp = []
    lst = []
    lst_cut = []

    soup = parser.parse()

    table = soup.find('tbody')
    table = table.find_next('tbody')
    tds = table.find_all('td')
    cntr = 0
    while cntr < len(tds):
        td = tds[cntr]
        lst.append(clear_text(td.text, ['strip']))
        cntr += 1
    for el in lst:
        index = lst.index(el)
        if index % 2 != 0:
            price = el
        else:
            title = el
            speed = el
        try:
            if title and speed and price:
                tarif_dic = {'title':title, 'speed':speed, 'price':price}
                all_tarifs.append(tarif_dic)
                title = speed = price = None
        except Exception as e:
            pass
    all_tarifs = all_tarifs[:-1]

    parser.set_tarifs(all_tarifs)
    return parser