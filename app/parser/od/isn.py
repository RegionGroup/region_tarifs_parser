import re

from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='ICN',
        url='http://icn.ua/prices',
        cnct_type=params['cnct_type'])

    all_tarifs = []
    lst = []
    tarif_dic = {}

    soup = parser.parse()

    def data_in_table(tr):

        for el in tr:
            tds = el.find_all('td')
            for td in tds:
                td = td.text
                td = clear_text(td, ['specials'])
                math = re.fullmatch(r'\w', td)
                if not math and td != 'Подключить' and td != ' ':
                    lst.append(td)
        cntr = 0
        while cntr < len(lst):
            cut_min = cntr
            cut_max = cntr + 3
            lst_cut = lst[cut_min:cut_max]
            title = lst[0]
            speed = f'{lst_cut[1]} Мбит/с'
            price = f'{lst_cut[2]} грн.'
            if title and speed and price:
                tarif_dic = {'title':title, 'speed':speed, 'price':price}
            all_tarifs.append(tarif_dic)
            cntr += 3

        return all_tarifs

    div = soup.find_all('table', attrs='table_center')

    if parser.get_cnct_type() == 'Акционные':
        competitor = parser.get_name() + ' Акционные'
        div = div[0]
        tr = div.find_all('tr', attrs='c-service')
        all_tarifs = data_in_table(tr)
    elif parser.get_cnct_type() == 'Интернет':
        competitor = parser.get_name() + ' Интернет'
        div = div[1]
        tr = div.find_all('tr', attrs='c-service')
        all_tarifs = data_in_table(tr)
    elif parser.get_cnct_type() == 'Интернет + TV':
        competitor = parser.get_name() + ' Интернет + TV'
        div = div[2]
        tr = div.find_all('tr', attrs='c-service')
        all_tarifs = data_in_table(tr)
    elif parser.get_cnct_type() == 'Интернет + TV + SIP':
        competitor = parser.get_name() + ' Интернет + TV + SIP'
        div = div[3]
        tr = div.find_all('tr', attrs='c-service')
        all_tarifs = data_in_table(tr)
    elif parser.get_cnct_type() == 'Elite':
        competitor = parser.get_name() + ' Elite'
        div = div[4]
        tr = div.find_all('tr', attrs='c-service')
        all_tarifs = data_in_table(tr)

    parser.set_name(competitor)
    parser.set_tarifs(all_tarifs)
    return parser