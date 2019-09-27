from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='Beetec',
        url='http://www.beetec.od.ua/price.php',
        habitation=params['habitation'])

    tarif_dic = {}
    all_tarifs = []
    all_tarifs_tmp = []
    lst = []

    soup = parser.parse()

    def extract_data(table):
        
        all_tarifs = []

        trs = table.find_all('tr')
        trs = trs[3:-1]

        for tr in trs:
            tds = tr.find_all('td')
            title = tds[1].text
            speed = tds[2].text
            price = tds[3].text
            price += 'грн/мес'

            if title and speed and price:
                tarif_dic = {'title':title, 'speed':speed, 'price':price}
            all_tarifs.append(tarif_dic)

        return all_tarifs

    div = soup.find(text='Тарифные планы Интернет и Телевидения для Дома:')

    table = div.parent.parent.parent.parent.next_sibling.next_sibling
    table_two = table.next_sibling.next_sibling.next_sibling.next_sibling
    table_three = table_two.next_sibling.next_sibling.next_sibling.next_sibling

    lst = [ table, table_two, table_three ]

    for table in lst:
        all_tarifs_tmp = extract_data(table)
        all_tarifs += all_tarifs_tmp

    parser.set_tarifs(all_tarifs)
    return parser