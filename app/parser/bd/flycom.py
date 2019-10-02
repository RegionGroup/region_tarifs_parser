from parser.parser import Parser


def trf_parser(**params):

    parser = Parser(
        name="Flycom",
        url=f'https://flycom.net.ua/?project={params["locality"]}',
        locality=params["locality"],
        cnct_type=params["cnct_type"],
    )

    soup = parser.parse()
    tarif_dic = {}
    all_tarifs = []
    all_tarifs_wifi = []

    if parser.get_cnct_type() == "cabel":

        div = soup.find("div", attrs="et_pb_pricing_1")
        title = div.find("h2", attrs="et_pb_pricing_title").text
        price = div.find("div", attrs="et_pb_pricing_content_top")
        price = price.find("span", attrs="et_pb_sum").text
        price += "грн/мес"
        ul = div.find("ul", attrs="et_pb_pricing")
        spans = ul.find_all("span")
        speed = spans[1].text

        if title and speed and price:
            tarif_dic = {"title": title, "speed": speed, "price": price}
        all_tarifs.append(tarif_dic)

        competitor = f"{parser.get_name()}-{parser.get_locality()}"
        parser.set_name(competitor)
        parser.set_tarifs(all_tarifs)
        return parser

    if parser.get_cnct_type() == "wi-fi":

        div = soup.find("div", attrs="et_pb_second_featured")
        divs = div.find_all("div", attrs="et_pb_pricing_table")
        for div in divs:
            title = div.find("h2", attrs="et_pb_pricing_title").text
            price = div.find("span", attrs="et_pb_sum").text
            price += "грн/мес"
            ul = div.find("ul", attrs="et_pb_pricing")
            spans = ul.find_all("span")
            speed = spans[1].text

            if title and speed and price:
                tarif_dic = {"title": title, "speed": speed, "price": price}
            all_tarifs_wifi.append(tarif_dic)

        competitor = (
            f"{parser.get_name()}-{parser.get_locality()} {parser.get_cnct_type()}"
        )
        parser.set_name(competitor)
        parser.set_tarifs(all_tarifs_wifi)
        return parser
