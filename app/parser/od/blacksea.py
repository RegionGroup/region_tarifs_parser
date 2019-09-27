from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='Blacksea',
        url='https://blacksea.net.ua/internet/?data-ft=0#div_for_uslugi',)

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()

    divs = soup.find_all('div', attrs='item_tarif')

    for div in divs:
        title = div.find('div', attrs='pop_tit_for').text
        price = div.find('i', attrs='t_price').text

        speed_wrp = div.find('div', attrs='razdel_pop')
        speed = speed_wrp.find('div', attrs='left_i_und3').text
        
        if title and speed and price:
            tarif_dic = {'title':title, 'speed':speed, 'price':price}
        all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser