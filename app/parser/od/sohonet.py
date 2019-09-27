from parser.parser import Parser
from parser.tools import clear_text

def trf_parser(**params):

    parser = Parser(
        name='Sohonet',
        url='https://sohonet.ua/services/internet',
        habitation=params['habitation'])

    if parser.get_habitation() == 'house':
        parser.set_name('Sohonet-house')
        parser.set_url('https://sohonet.ua/services/internet/private')
    elif parser.get_habitation() == 'community':
        parser.set_name('Sohonet-community')
        parser.set_url('https://sohonet.ua/services/internet/student')

    tarif_dic = {}
    all_tarifs = []

    soup = parser.parse()

    try:
        trf_yearly  = soup.find('div', attrs='wrap_goodYear')
        trf_yearly_title = trf_yearly.find('div', attrs='text_title').text

        speed_wrp = trf_yearly.find('div', attrs='name_inet')
        trf_yearly_speed = speed_wrp.find('div', attrs='text_value').text

        speed_wrp = trf_yearly.find('div', attrs='name_price')
        trf_yearly_price = speed_wrp.find('div', attrs='text_value').text

        if trf_yearly_title and trf_yearly_speed and trf_yearly_price:
            tarif_dic = {'title':trf_yearly_title, 'speed':trf_yearly_speed, 'price':trf_yearly_price}
        all_tarifs.append(tarif_dic)
    except Exception as e:
        pass

    cont  = soup.find('div', attrs='wrap_triPlan')
    divs  = soup.find_all('div', attrs='item_plan')
    for div in divs:

        disabled_div = None
        try:
            disabled_div = div.find('div', attrs='wrap_disabled')
        except Exception as e:
            pass

        if disabled_div:
            pass
        else:
            title = div.find('div', attrs='text_planTitle').text
            title = clear_text(title, ['full'])

            speed_wrp = div.find('div', attrs='name_inet')
            speed = speed_wrp.find('div', attrs='text_value').text
            speed =clear_text(speed, ['full'])
            
            price_wrp = div.find('div', attrs='name_price')
            price = price_wrp.find('div', attrs='text_value').text
            price = clear_text(price, ['full'])
                        
            if title and speed and price:
                tarif_dic = {'title':title, 'speed':speed, 'price':price}
            all_tarifs.append(tarif_dic)

    parser.set_tarifs(all_tarifs)
    return parser