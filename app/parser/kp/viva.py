import math

from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='VI-VA',
        url='http://vi-va.com.ua/services.php?id=7',)

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()

    paragraphs = soup.find_all('p', attrs='p_terif')
    for el in paragraphs:
        if el:
            el = el.text
            el = clear_text(el, ['strip'])
        if el == '-----':
            el = 'Не указана'
        all_tarifs.append(el)

    mltpl_three = all_tarifs[18:]
    all_tarifs = []

    cntr = cut_min = 0
    limit = math.trunc(len(mltpl_three)/3)
    while cntr < limit:
        cut_max = cut_min + 3
        tarif_prcs_spd_lst = mltpl_three[cut_min:cut_max]
        title = tarif_prcs_spd_lst[0]
        speed = tarif_prcs_spd_lst[0]
        price = tarif_prcs_spd_lst[1]
        if title and speed and price:
            tarif_dic = {'title':title, 'speed':speed, 'price':price}
        all_tarifs.append(tarif_dic)
        cut_min = cut_max
        cntr += 1

    parser.set_tarifs(all_tarifs)
    return parser