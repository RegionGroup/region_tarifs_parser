from parser.parser import DinamicParser
from parser.tools import clear_text

def trf_parser(**params):

    parser = DinamicParser(
        name='Setka',
        url='http://setka.od.ua/tarif_home_new',)

    tarif_dic = {}
    all_tarifs = []
    all_tarifs_tmp = []

    def extract_data(div):
        all_tarifs = []
        divs = div.find_all('div')
        for div in divs:
            try:
                title = div.find('h2').text
                price = div.find('h1').text
                price += 'грн/мес'
                li = div.find_all('li')
                speed = li[2].text
                if title and speed and price:
                    tarif_dic = {'title':title, 'speed':speed, 'price':price}
                all_tarifs.append(tarif_dic)
            except Exception as e:
                pass
        return all_tarifs

    soup = parser.parse()
    div = soup.find('div', id='tab_home_2019')
    all_tarifs_tmp = extract_data(div)
    all_tarifs += all_tarifs_tmp
    div = soup.find('div', id='tab_odessa_copper_complex_2019')
    all_tarifs_tmp = extract_data(div)
    all_tarifs += all_tarifs_tmp

    parser.set_tarifs(all_tarifs)
    return parser