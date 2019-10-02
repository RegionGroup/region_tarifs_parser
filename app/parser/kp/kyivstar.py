from parser.parser import DinamicParser
from parser.tools import clear_text


def trf_parser(**params):

    parser = DinamicParser(name="Kyivstar", url="https://kyivstar-home-internet.com.ua")

    tarif_dic = {}
    all_tarifs = []
    all_tarifs_tmp = []
    lst = []

    def extract_data(div):
        all_tarifs = []
        title = div.find("div", attrs="rates__title").text
        title = clear_text(title, ["strip"])
        ul = div.find("ul", attrs="rates__details")
        for li in ul:
            try:
                value = li.find("div", attrs="option__value").text
                lst.append(value)
            except Exception as e:
                pass
        speed = lst[0]
        speed = clear_text(speed, ["strip"])
        speed += "Мб/сек"
        price = div.find("div", attrs="price-new").text
        price += "грн/мес"
        price = clear_text(price, ["strip"])
        if title and speed and price:
            tarif_dic = {"title": title, "speed": speed, "price": price}
        all_tarifs.append(tarif_dic)
        return all_tarifs

    soup = parser.parse()

    divs = soup.find_all("div", attrs="rates__item")

    for div in divs:
        all_tarifs_tmp = extract_data(div)
        all_tarifs += all_tarifs_tmp

    parser.set_tarifs(all_tarifs)
    return parser
