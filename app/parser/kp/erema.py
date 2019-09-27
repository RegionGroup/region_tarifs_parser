import re

from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='Erema',
        url='http://www.erema.net.ua/index.php/features',)

    tarif_dic = {}
    all_tarifs= []
    lst = []

    soup = parser.parse()

    tds = soup.find_all('td', style='text-align: center;')

    for td in tds:
        td = td.text
        match = re.fullmatch(r'\w', td) or re.search(r'[\n]', td)
        if not match:
            lst.append(td)

    for el in lst:
        index = lst.index(el)
        if index % 2 != 0:
            title = el
            speed = el
        else:
            price = el

        try:
            if title and speed and price:
                tarif_dic = {'title':title, 'speed':speed, 'price':price}
                all_tarifs.append(tarif_dic)
                title = speed = price = None
        except Exception as e:
            pass

    parser.set_tarifs(all_tarifs)
    return parser