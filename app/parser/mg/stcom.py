from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='СТком',
        url='https://st.marganets.net/uk/internet/#',
        habitation=params['habitation'])

    if parser.get_habitation() == 'aprtmnt':
        mod_url = 'kvarturu'
    if parser.get_habitation() == 'house':
        mod_url = 'pruvatnui_sektor'

    base_url = f'{parser.get_url()}{mod_url}'
    parser.set_url(base_url)

    tarif_dic = {}
    all_tarifs = []
    all_tarifs_aprtmnt = []
    all_tarifs_house = []

    soup = parser.parse()

    divs = soup.find_all('div', attrs='gw-go-col-inner')
    divs = divs[1:]

    for div in divs:
        title_wrpr = div.find('div', attrs='gw-go-header-top')
        if title_wrpr:
            title = title_wrpr.find('h3').text

        speed_tmp = div.find('div', attrs='gw-go-body-cell').text
        if len(speed_tmp) <= 13:
            speed = speed_tmp

        price_wrpr = div.find('div', attrs='gw-go-price-wrap')
        if price_wrpr:
            price = price_wrpr.find('span').text
            price += 'грн/мсц'

        try:
            if title and speed and price:
                tarif_dic = {'title':title, 'speed':speed, 'price':price}
            all_tarifs.append(tarif_dic)
        except Exception as e:
            pass

    del all_tarifs[3]
    all_tarifs_house = all_tarifs[3:]
    del all_tarifs[3:]
    all_tarifs_aprtmnt = all_tarifs

    competitor_aprtmnt = f'{parser.get_name()}-многоквартирные дома'
    competitor_house = f'{parser.get_name()}-частный сектор'

    if parser.get_habitation() == 'aprtmnt':
        parser.set_name(competitor_aprtmnt)
        parser.set_tarifs(all_tarifs_aprtmnt)
        return parser
    if parser.get_habitation() == 'house':
        parser.set_name(competitor_house)
        parser.set_tarifs(all_tarifs_house)
        return parser