from parser.parser import Parser
from parser.tools import clear_text


def trf_parser(**params):

    parser = Parser(
        name="Prostor", url="http://prostor.net.ua/tarif", cnct_type=params["cnct_type"]
    )

    tarif_dic = {}
    all_tarifs = []
    all_tarifs_wifi = []

    soup = parser.parse()

    table = soup.find("table")
    tds = table.find_all("td")

    title = tds[1].text
    speed = tds[1].text
    price = tds[2].text
    if title and speed and price:
        tarif_dic = {"title": title, "speed": speed, "price": price}

    all_tarifs.append(tarif_dic)

    table_two = table.find_next("table")
    tds = table_two.find_all("td")
    del tds[-1]
    del tds[-2]

    lst = []
    for td in tds:
        index = tds.index(td)
        if index % 3 != 0:
            lst.append(td.text)

    cntr = 0
    while cntr < len(lst):
        title = lst[cntr]
        speed = lst[cntr]
        price = lst[cntr + 1]
        if title and speed and price:
            tarif_dic = {"title": title, "speed": speed, "price": price}
        all_tarifs_wifi.append(tarif_dic)
        cntr += 2

    if parser.get_cnct_type() == "cabel":
        parser.set_tarifs(all_tarifs)
        return parser
    if parser.get_cnct_type() == "wi-fi":
        competitor = f"{parser.get_name()} {parser.get_cnct_type()}"
        parser.set_name(competitor)
        parser.set_tarifs(all_tarifs_wifi)
        return parser

    parser.set_tarifs(all_tarifs)
    return parser
