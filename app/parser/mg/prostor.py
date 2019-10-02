from time import sleep

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

import conf
from parser.parser import DinamicParser
from parser.tools import clear_text


class Prostor(DinamicParser):
    def __init__(self, **kwargs):
        super(Prostor, self).__init__(**kwargs)
        self.__tarifs = []
        self.__param = kwargs

    def pick_city(self, browser, city, id):
        loc = f"-{city}"
        gorodishe = browser.find_element_by_xpath(f'//li[@data-town-id="{id}"]').click()
        sleep(10)
        generated_html = browser.page_source
        browser.quit()
        return loc, generated_html

    def parse(self, city, competitor):
        pr_delay = 3
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        # options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(
            chrome_options=options, executable_path=conf.PATH_TO_CHROMEDRIVER
        )
        browser.get(self.get_url())
        sleep(20)
        try:
            close = browser.find_element_by_xpath(
                '//button[@class="sendpulse-prompt-close"]'
            ).click()
        except Exception as e:
            pass
        sleep(pr_delay)
        try:
            close = browser.find_element_by_id("confirm-town-times").click()
        except Exception as e:
            pass
        sleep(5)
        try:
            close = browser.find_element_by_xpath(
                '//span[@class="b24-widget-button-popup-btn-hide"]'
            ).click()
        except Exception as e:
            pass
        sleep(pr_delay)
        pick = browser.find_element_by_xpath('//h5[@class="town-text-pick"]//a').click()
        sleep(pr_delay)
        ul = browser.find_element_by_xpath(
            '//ul[@class="region-items-wrap"]//li[1]'
        ).click()
        sleep(pr_delay)

        if city == "Городище":
            loc, generated_html = self.pick_city(browser, "Городище", "9833")
            competitor += loc
        elif city == "Закамянка":
            loc, generated_html = self.pick_city(browser, "Закамянка", "7294")
            competitor += loc
        elif city == "Максимівка":
            loc, generated_html = self.pick_city(browser, "Максимівка", "7293")
            competitor += loc
        elif city == "Марьивка":
            loc, generated_html = self.pick_city(browser, "Марьивка", "7285")
            competitor += loc
        elif city == "Новоселівка":
            loc, generated_html = self.pick_city(browser, "Новоселівка", "9725")
            competitor += loc
        elif city == "Остров":
            loc, generated_html = self.pick_city(browser, "Остров", "7288")
            competitor += loc
        else:
            print("Не верный город")
        return bs(generated_html, "lxml"), competitor


def trf_parser(**params):

    parser = Prostor(
        name="Prostor",
        url="https://prosto.net/our-plans/",
        locality=params["locality"],
        cnct_type=params["cnct_type"],
    )

    city = parser.get_locality()
    competitor = parser.get_name()

    tarif_dic = {}
    all_tarifs = []
    lst_title = []
    lst_speed = []
    lst_price = []

    pr_delay = 3

    soup, competitor = parser.parse(city, competitor)

    def extract_date(tarifs_div):
        divs = tarifs_div.find_all("div", attrs="tarif-stripe")
        for div in divs:
            try:
                title = div.find("h4").text
                lst_title.append(title)
            except Exception as e:
                pass

        divs = tarifs_div.find_all("div", attrs="tarif-row")
        for div in divs:
            price = div.find("p", attrs="tarif-price").text
            price += "грн/мес"
            lst_price.append(price)
            speed = div.find("p", attrs="speed-circle-number").text
            speed = clear_text(speed, ["line breaks"])
            lst_speed.append(speed)

        cntr = 0
        while cntr < len(lst_title):
            title = lst_title[cntr]
            speed = lst_speed[cntr]
            price = lst_price[cntr]
            if title and speed and price:
                tarif_dic = {"title": title, "speed": speed, "price": price}
            all_tarifs.append(tarif_dic)
            cntr += 1
        return all_tarifs

    tarifs = soup.find("article")

    if parser.get_cnct_type() == "cabel":
        competitor += "-cabel"
        tarifs_div = tarifs.find("div", attrs="ftth")
    elif parser.get_cnct_type() == "wi-fi":
        competitor += "-wi-fi"
        tarifs_div = tarifs.find("div", attrs="prewimax")

    all_tarifs = extract_date(tarifs_div)
    parser.set_name(competitor)
    parser.set_tarifs(all_tarifs)
    return parser
