from parser.parser import Parser
from parser.tools import clear_text


def trf_parser(**params):

    parser = Parser(
        name="Infomir",
        url="http://www.infomir.com.ua/tariff/internet/",
        habitation=params["habitation"],
    )

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()
    table = soup.find("table")
    columns = table.findAll("div", attrs="column")

    for col in columns:
        title_div = col.find("div", attrs="header-tariff-name")
        title = title_div.find("p").text
        price_div = col.find("div", attrs="column-tariff-label")
        price = price_div.find("span").text
        speed_div = (
            col.find("div", attrs="header-tariff-name")
            .find_next("div")
            .find_next("div")
        )
        speed = speed_div.find("strong").text
        tarif_dic = {"title": title, "speed": speed, "price": price}
        all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser
