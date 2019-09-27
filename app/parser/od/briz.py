from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='Briz',
        url='https://www.briz.ua/domashniy-internet/#monthly',)

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()

    titles = soup.find_all('p', attrs='internet-for-home-prise-list-text-align-center')
    speeds = soup.find_all('div', attrs='internet-for-home-prise-list-right-div')

    i = 0
    while i < len(titles):
        title = clear_text(titles[i].text.strip(), ['full'])
        speed = clear_text(speeds[i].text.strip(), ['full'])
        if title and speed:
            tarif_dic = {'title':title, 'speed':speed}
            all_tarifs.append(tarif_dic)
        i += 1

    parser.set_tarifs(all_tarifs)
    return parser