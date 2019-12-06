from parser.parser import Parser
from parser.tools import clear_text


def trf_parser(**params):

    parser = Parser(
        name="Vega",
        url="https://vega.ua/rus/for_home/superconnect_fttb",
        habitation=params["habitation"],
    )

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()
    main_div = soup.find("div", attrs="blockID1201").text.strip()
    all_tarifs = [{"title": main_div}]
    parser.set_tarifs(all_tarifs)
    return parser
