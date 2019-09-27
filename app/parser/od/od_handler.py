import conf

from parser.parser import Parser
from gdoc.gdoc import Gdoc

import parser.od.tenet as tenet
import parser.od.sohonet as sohonet
import parser.od.vega as vega
import parser.od.blacksea as blacksea
import parser.od.isn as isn
import parser.od.briz as briz
import parser.od.beetec as beetec
import parser.od.lionline as lionline
import parser.od.spider as spider
import parser.od.setka as setka
import parser.od.ukrtelecom as ukrtelecom
import parser.od.intertelecom as intertelecom
import parser.od.infomir as infomir
import parser.od.westele as westele
import parser.od.kyivstar as kyivstar
import parser.od.vodafone as vodafone
import parser.od.triolan as triolan

od_errors = []
gdocInst = Gdoc(conf.PATH_TO_CRED)

def add_error(error_log):
    od_errors.append(error_log)

def get_parser_instance(parser, locality=None, cnct_type=None, habitation=None, coordinates=None):
    try:
        parserInst = parser.trf_parser(
            locality=locality, cnct_type=cnct_type, 
            habitation=habitation, coordinates=coordinates)
        if Parser in parserInst.__class__.__mro__:
            return parserInst
        else:
            add_error(f'Парсер "{parser.__name__}" Error "parserInst is not Parser-class"')
    except Exception as e:
        add_error(f'Парсер "{parser.__name__}" вернул ошибку: {e}')

def write_to_gdoc(parserInst):
    gdocInst.g_sheets_update(parserInst, conf.OD_GDOC)

def main():

    # Tenet
    tenet_inst = get_parser_instance(tenet, cnct_type='cabel')
    write_to_gdoc(tenet_inst) if tenet_inst else print(f'{tenet.__name__} Error')

    # Sohonet
    sohonet_inst = get_parser_instance(sohonet)
    write_to_gdoc(sohonet_inst) if sohonet_inst else print(f'{sohonet.__name__} Error')

    # Sohonet-house
    sohonet_inst = get_parser_instance(sohonet, habitation='house')
    write_to_gdoc(sohonet_inst) if sohonet_inst else print(f'{sohonet.__name__} Error')

    # Sohonet-community
    sohonet_inst = get_parser_instance(sohonet, habitation='community')
    write_to_gdoc(sohonet_inst) if sohonet_inst else print(f'{sohonet.__name__} Error')

    # Vega
    vega_inst = get_parser_instance(vega)
    write_to_gdoc(vega_inst) if vega_inst else print(f'{vega.__name__} Error')

    # Blacksea
    blacksea_inst = get_parser_instance(blacksea)
    write_to_gdoc(blacksea_inst) if blacksea_inst else print(f'{blacksea.__name__} Error')

    # ISN
    isn_inst = get_parser_instance(isn, cnct_type='Интернет')
    write_to_gdoc(isn_inst) if isn_inst else print(f'{isn.__name__} Error')
    isn_inst = get_parser_instance(isn, cnct_type='Интернет + TV')
    write_to_gdoc(isn_inst) if isn_inst else print(f'{isn.__name__} Error')
    isn_inst = get_parser_instance(isn, cnct_type='Интернет + TV + SIP')
    write_to_gdoc(isn_inst) if isn_inst else print(f'{isn.__name__} Error')
    isn_inst = get_parser_instance(isn, cnct_type='Elite')
    write_to_gdoc(isn_inst) if isn_inst else print(f'{isn.__name__} Error')

    # Briz
    briz_inst = get_parser_instance(briz, cnct_type='Elite')
    write_to_gdoc(briz_inst) if briz_inst else print(f'{briz.__name__} Error')

    # Beetec
    beetec_inst = get_parser_instance(beetec, cnct_type='Elite')
    write_to_gdoc(beetec_inst) if beetec_inst else print(f'{beetec.__name__} Error')

    # Lionline
    lionline_inst = get_parser_instance(lionline, cnct_type='Elite')
    write_to_gdoc(lionline_inst) if lionline_inst else print(f'{lionline.__name__} Error')

    # Spider
    spider_inst = get_parser_instance(spider, cnct_type='Elite')
    write_to_gdoc(spider_inst) if spider_inst else print(f'{spider.__name__} Error')

    # Setka
    setka_inst = get_parser_instance(setka, cnct_type='Elite')
    write_to_gdoc(setka_inst) if setka_inst else print(f'{setka.__name__} Error')

    # Ukrtelecom - Одесса
    ukrtelecom_inst = get_parser_instance(ukrtelecom, coordinates=[1249, 1275, 10179, 'Одесса'])
    write_to_gdoc(ukrtelecom_inst) if ukrtelecom_inst else print(f'{ukrtelecom.__name__} Error')

    # Intertelecom
    intertelecom_inst = get_parser_instance(intertelecom, coordinates=[1249, 1275, 10179, 'Одесса'])
    write_to_gdoc(intertelecom_inst) if intertelecom_inst else print(f'{intertelecom.__name__} Error')

    # Infomir
    infomir_inst = get_parser_instance(infomir)
    write_to_gdoc(infomir_inst) if infomir_inst else print(f'{infomir.__name__} Error')

    # Westele
    westele_inst = get_parser_instance(westele)
    write_to_gdoc(westele_inst) if westele_inst else print(f'{westele.__name__} Error')

    # Kyivstar
    kyivstar_inst = get_parser_instance(kyivstar)
    write_to_gdoc(kyivstar_inst) if kyivstar_inst else print(f'{westkyivstarele.__name__} Error')

    # Vodafone
    vodafone_inst = get_parser_instance(vodafone)
    write_to_gdoc(vodafone_inst) if vodafone_inst else print(f'{vodafone.__name__} Error')

    # Triolan
    triolan_inst = get_parser_instance(triolan)
    write_to_gdoc(triolan_inst) if triolan_inst else print(f'{triolan.__name__} Error')

    gdocInst.g_sheets_errorlog(od_errors, conf.OD_GDOC)