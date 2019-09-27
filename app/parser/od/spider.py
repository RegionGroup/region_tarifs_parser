from parser.parser import DinamicParser
from parser.tools import clear_text

def trf_parser(**params):

    parser = DinamicParser(
        name='Spider',
        url='https://spider-net.od.ua/uslugi-i-tarify/#1',)

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()

    cont = soup.find('div', attrs='column2')
    four_col = cont.find('div', attrs='four_columns')
    divs = four_col.find_all('div', attrs='column_inner')
    for div in divs:

        title_wrp = div.find('h4')
        title = clear_text(title_wrp.text, ['strip'])
        price = div.find('td').text
        price = clear_text(price, ['line breaks', 'strip'])
        price_stable = price[:-3]
        price_disc = price[-3:]
        price = f'{price_stable} при заказе специальных предложений: {price_disc}'
        speed = title_wrp.find_next('h4').text

        if title and speed and price:
            tarif_dic = {'title':title, 'speed':speed, 'price':price}
        all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser 