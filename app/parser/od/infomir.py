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

    def infomir_parse_table(table, price_position):
        all_tarifs = []
        coll_cntr = 1
        while coll_cntr < 4:
            rows = table.findAll("tr")
            fs_row = rows[0]
            fs_col = fs_row.findAll("td")
            fs_col = fs_col[coll_cntr].text
            title = fs_col

            fs_row = rows[1]
            fs_col = fs_row.findAll("td")
            fs_col = fs_col[coll_cntr].text
            speed = fs_col

            fs_row = rows[price_position]
            fs_col = fs_row.findAll("td")
            fs_col = fs_col[coll_cntr]
            fs_col = fs_row.findAll("div")
            fs_col = fs_col[coll_cntr].text
            price = fs_col

            coll_cntr += 1

            tarif_dic = {"title": title, "speed": speed, "price": price}
            all_tarifs.append(tarif_dic)
        return all_tarifs

    soup = parser.parse()
    table = soup.find("table")
    table = table.find("table")
    table = table.findAll("table")

    first_table = table[5]
    fs_price_position = 9
    two_table = table[6]
    tw_price_position = 8

    ft_tarifs = infomir_parse_table(first_table, fs_price_position)
    tt_tarifs = infomir_parse_table(two_table, tw_price_position)
    all_tarifs = ft_tarifs + tt_tarifs

    parser.set_tarifs(all_tarifs)
    return parser
