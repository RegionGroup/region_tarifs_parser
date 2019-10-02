from parser.parser import Parser
from parser.tools import clear_text


def trf_parser(**params):

    parser = Parser(
        name="kup.mytelecom.ua",
        url="https://kup.mytelecom.ua/#mytele",
        locality="kupyansk",
        habitation=params["habitation"],
    )

    tarif_dic = {}
    all_tarifs = []
    all_tarifs_tmp = []

    soup = parser.parse()
    divs = soup.find_all("ul", attrs="gw-go-body")
    for div in divs:
        cells = div.find_all("div", attrs="gw-go-body-cell")
        title = ""
        for cell in cells:
            title += cell.text.strip()

        tarif_dic = {"title": title}
        all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser
