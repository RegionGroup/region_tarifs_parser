from parser.parser import Parser
from parser.tools import clear_text


def trf_parser(**params):

    parser = Parser(name="Kyivstar-fmc", url="https://kyivstar.ua/uk/fmc")

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()

    divs = soup.find_all("div", attrs="swiper-slide")
    for div in divs:

        title = div.find("div", attrs="fmc-tariff-item-new__name").text
        sub_title = div.find("div", attrs="fmc-tariff-item-new__name-subtitle").text
        title = f"{title}: {sub_title}"
        title = clear_text(title, ["strip"])
        speed = div.find("div", attrs="fmc-tariff-item-new__bold-title").text
        speed = clear_text(speed, ["strip"])
        price = div.find("div", attrs="fmc-tariff-item-new__current").text
        price += " грн/мсц"
        price = clear_text(price, ["strip"])

        if title and speed and price:
            tarif_dic = {"title": title, "speed": speed, "price": price}
        all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser
