from parser.parser import DinamicParser
from parser.tools import clear_text

def trf_parser(**params):

    parser = DinamicParser(
        name='Westele',
        url='https://westele.com.ua/ru/service/home/internet',)

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()

    div = soup.find('ul', attrs='speedItems')
    lis = div.find_all('li', attrs='itemSpeed')

    for li in lis:
        speed = li.find("li", "headSpeed")
        speed = speed.find("span").text
        speed += "Мбит/сек"

        title = speed

        price = li.find("li", "priceSpeed")
        price = price.find("span").text
        price += 'грн/мес'

        if title and speed and price:
            tarif_dic = {'title':title, 'speed':speed, 'price':price}
        all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser