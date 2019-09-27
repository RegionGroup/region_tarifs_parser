from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='Tenet',
        url='https://www.tenet.ua/dlya-doma/internet/',
        cnct_type=params['cnct_type'])

    if parser.get_cnct_type() == 'cabel':
        mod_url = f'{parser.get_url()}tarify'
        parser.set_url(mod_url)
    elif parser.get_cnct_type() == 'wi-fi':
        mod_url = f'{parser.get_url()}besprovodnoy-internet/besprovodnoy-internet-v-chastnom-sektore'
        parser.set_url(mod_url)
        parser.set_name('Tenet-wifi')

    tarif_dic = {}
    all_tarifs = []
    titles_list = []
    prices_list = []
    speeds_list = []

    soup = parser.parse()
    table = soup.find('table', attrs='views-table')
    thead = table.find('thead')

    thead = thead.findAll('th')
    for th in thead:
        th = th.text
        th = clear_text(th, ['strip', 'specials'])
        if th != "":
            titles_list.append(th)
    tbody = table.find('tbody')
    tbody = table.findAll('tr')[2]
    tr = tbody.findAll('td')
    for td in tr:
        td = td.text
        td = clear_text(td, ['strip', 'specials'])
        if td != "":
            prices_list.append(td)			
    tbody = table.findAll('tr')[3]
    tr = tbody.findAll('td')
    for td in tr:
        td = td.text
        td = clear_text(td, ['strip', 'specials'])
        if td != "":
            speeds_list.append(td)
    titles_count = len(titles_list)
    i = 0
    while i < titles_count:
        title = titles_list[i]
        speed = speeds_list[i]
        price = prices_list[i]
        tarif_dic = {'title':title, 'speed':speed, 'price':price}
        all_tarifs.append(tarif_dic)
        i += 1

    parser.set_tarifs(all_tarifs)
    return parser