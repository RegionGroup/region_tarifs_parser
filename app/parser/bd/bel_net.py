from parser.parser import Parser


def trf_parser(**params):

    parser = Parser(
        name="Bel.net.ua-shabo",
        url="https://bel.net.ua/coating/odesskaia-oblast/belgorod-dnestrovskii-raion/shabo",
        cnct_type=params["cnct_type"],
    )

    soup = parser.parse()
    tarif_dic = {}
    all_tarifs_wifi = []

    divs = soup.find_all("article", attrs="coating-page-item")
    for div in divs:
        title = div.find("h2").text
        span = div.find_all("span", attrs="value")
        speed = span[0].text
        price = span[1].text

        if title and speed and price:
            tarif_dic = {"title": title, "speed": speed, "price": price}
        all_tarifs_wifi.append(tarif_dic)

    competitor = f"{parser.get_name()} {parser.get_cnct_type()}"
    parser.set_name(competitor)
    parser.set_tarifs(all_tarifs_wifi)
    return parser
