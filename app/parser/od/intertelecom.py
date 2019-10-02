import conf

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

from parser.parser import DinamicParser
from parser.tools import clear_text

delay = 8


class Intertelecom(DinamicParser):
    def __init__(self, **kwargs):
        super(Intertelecom, self).__init__(**kwargs)
        self.__tarifs = []
        self.__param = kwargs

    def parse(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(
            chrome_options=options, executable_path=conf.PATH_TO_CHROMEDRIVER
        )
        browser.get(self.get_url())
        sleep(delay)
        button = browser.find_element_by_xpath(
            '//button[@class="btn dropdown-toggle btn-default"]'
        ).click()
        sleep(delay)
        li = browser.find_element_by_xpath(f'//li[@data-original-index="3"]').click()
        sleep(delay)
        generated_html = browser.page_source
        browser.quit()
        return bs(generated_html, "lxml")


def trf_parser(**params):

    parser = Intertelecom(
        name="intertelecom.ua", url="https://www.intertelecom.ua/home_internet_wifi"
    )

    tarif_dic = {}
    all_tarifs = []

    def extract_data(div):
        all_tarifs = []

        title = div.find("h4").text
        li = div.find("li")
        li = li.find_next("li")
        price = li.find("div", "description-option").text
        if title and price:
            tarif_dic = {"title": title, "price": price}
        all_tarifs.append(tarif_dic)
        return all_tarifs

    soup = parser.parse()

    cont = soup.find("div", attrs="slick-track")
    divs = cont.find_all("div", attrs="tariff-item")

    for div in divs:
        all_tarifs_tmp = extract_data(div)
        all_tarifs += all_tarifs_tmp

    parser.set_tarifs(all_tarifs)
    return parser
