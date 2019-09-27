from parser.parser import DinamicParser
from parser.tools import clear_text

def trf_parser(**params):

    parser = DinamicParser(
        name='Kyivstar',
        url='https://internet-kyivstar.com.ua/tariffs-ru/',)

    tarif_dic = {}
    all_tarifs= []
    soup = parser.parse()

    divs = soup.find_all('div', attrs='item', limit=3)
    for el in divs:

        title = el.find('a', attrs='name')
        if title:
            title = title.text

        speed_val = el.find('span', attrs='speed-value')
        if speed_val:
            speed_val = speed_val.text
        speed_rem = el.find('span', attrs='value-rem')
        if speed_rem:
            speed_rem = speed_rem.text
        speed = speed_val + speed_rem

        price = el.find('div', attrs='cost')
        if price:
            price = price.text

        if title and speed and price:
            tarif_dic = {'title':title, 'speed':speed, 'price':price}
        all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser