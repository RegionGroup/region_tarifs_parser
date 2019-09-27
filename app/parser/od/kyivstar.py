from parser.parser import DinamicParser
from parser.tools import clear_text

def trf_parser(**params):

    parser = DinamicParser(
        name='kyivstar.ua/ru/home-kyivstar/internet/odesa',
        url='https://kyivstar.ua/ru/home-kyivstar/internet/odesa',)

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()

    title = soup.find('p', attrs='discount-promo__info').text
    price = soup.find('span', attrs='tariff-price-block__value').text
    price += 'грн/мес'

    if title and price:
        tarif_dic = {'title':title, 'price':price}
    all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser