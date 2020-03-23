from parser.parser import Parser
from parser.tools import clear_text


def trf_parser(**params):

    parser = Parser(
        name="Beetec",
        url="http://www.beetec.od.ua/price.php",
        habitation=params["habitation"],
    )

    tarif_dic = {}
    all_tarifs = []
    soup = parser.parse()

    divs = soup.findAll("div", attrs="tarif_dop")
    for div in divs:
        title = div.find("h3").text
        price = div.find("div", attrs="tarif_price1").text
        speed = div.find("div", attrs="tarif_speed").text
        if title and speed and price:
            tarif_dic = {'title': title, 'speed': speed, 'price': price}
        all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser
