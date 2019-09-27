from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='lionline',
        url='http://lionline.net.ua/tarif/',)

    tarif_dic = {}
    all_tarifs = []
    all_tarifs_tmp = []

    def extract_data(divs):
        all_tarifs = []
        for div in divs[2:]:
            title = div.find('div', 'ptsEl')

            price = div.find('div', 'ptsToggle')
            price_wrp = price.find_next('div', 'ptsToggle')
            price = price_wrp.find('div', 'ptsEl')

            speed = price.find_next('div', 'ptsEl')

            title = title.text
            price = price.text
            speed = speed.text

            if title and speed and price:
                tarif_dic = {'title':title, 'speed':speed, 'price':price}
            all_tarifs.append(tarif_dic)
        return all_tarifs

    soup = parser.parse()

    div = soup.find('div', attrs='ptsContainer')
    divs = div.find_all('div', attrs='ptsTableElementContent')

    all_tarifs_tmp = extract_data(divs)
    all_tarifs += all_tarifs_tmp

    div = div.find_next('div', attrs='ptsContainer')
    divs = div.find_all('div', attrs='ptsTableElementContent')

    all_tarifs_tmp = extract_data(divs)
    all_tarifs += all_tarifs_tmp

    parser.set_tarifs(all_tarifs)
    return parser