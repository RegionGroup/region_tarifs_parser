from parser.parser import Parser
from parser.tools import clear_text


def trf_parser(**params):

    parser = Parser(
        name="Mytelecom",
        url="https://mytelecom.ua/tarifs/kupyansk.php#OPTIC100OPT",
        locality="kupyansk",
        habitation=params["habitation"],
    )

    tarif_dic = {}
    all_tarifs = []
    titles_lst = []

    soup = parser.parse()

    divs = soup.find_all("div", attrs="tarif_content")
    for div in divs:
        title = div.find("h1").text
        if title != "Другие услуги":
            titles_lst.append(title)
        cont = div.find_all(True, {"class": ["c2", "c3"]})

        for el in cont:
            for tag in el:
                tag = clear_text(str(tag), ["strip"])
                if tag != "<br/>":
                    all_tarifs.append(tag)

        prcs_spd_lst_tmp = []
        a = ""
        for el in all_tarifs:
            if el == a:
                pass
            else:
                prcs_spd_lst_tmp.append(el)
            a = el

        prcs_spd_lst = []

        switch = False
        for el in prcs_spd_lst_tmp:
            if not switch:
                a = el
            if switch:
                b = el
                if a != b:
                    c = a + b
                else:
                    c = a
                prcs_spd_lst.append(c)
            switch = not switch

    all_tarifs = []
    cntr = 0
    while cntr < len(titles_lst):

        title = titles_lst[cntr]
        speed = prcs_spd_lst[cntr * 2]
        price = prcs_spd_lst[cntr * 2 + 1]

        if title and speed and price:
            tarif_dic = {"title": title, "speed": speed, "price": price}
        all_tarifs.append(tarif_dic)

        cntr += 1

    competitor_aprtmnt = f"{parser.get_name()}-многоквартирные дома"
    competitor_house = f"{parser.get_name()}-частный сектор"

    all_tarifs_aprtmnt = all_tarifs[0:2]
    all_tarifs_house = all_tarifs[2:]

    if parser.get_habitation() == "aprtmnt":
        parser.set_name(competitor_aprtmnt)
        parser.set_tarifs(all_tarifs_aprtmnt)
        return parser
    if parser.get_habitation() == "house":
        parser.set_name(competitor_house)
        parser.set_tarifs(all_tarifs_house)
        return parser
