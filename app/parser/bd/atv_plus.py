from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='АТВ+',
        url='http://atv-plus.net/?page_id=40',)

    soup = parser.parse()
    all_tarifs = []
    if soup:
        div = soup.find('div', attrs='entry-content')
        tables = div.find_all('table')
        tables_cut = tables[1:]
        table = tables_cut[0]
        table_str = table.text
        table = table_str.splitlines()
        table = list(filter(None, table))

        cntr = 3
        while cntr < len(table):
            cut_min = cntr
            cut_max = cntr + 3
            tarif_prcs_spd_lst = table[cut_min:cut_max]
            title = clear_text(tarif_prcs_spd_lst[0], ['strip'])
            speed = clear_text(tarif_prcs_spd_lst[1], ['strip'])
            price = clear_text(tarif_prcs_spd_lst[2], ['strip'])
            if title and speed and price:
                tarif_dic = {'title':title, 'speed':speed, 'price':price}
            all_tarifs.append(tarif_dic)
            cntr += 3

        parser.set_tarifs(all_tarifs)
        return parser