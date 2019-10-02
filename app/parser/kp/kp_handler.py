import conf

from parser.parser import Parser, DinamicParser
from gdoc.gdoc import Gdoc

import parser.kp.mytelecom as mytelecom
import parser.kp.viva as viva
import parser.kp.prostor as prostor
import parser.kp.erema as erema
import parser.kp.kyivstar as kyivstar
import parser.kp.ukrtelecom as ukrtelecom
import parser.kp.kupmytelecom as kupmytelecom

kp_errors = []
gdocInst = Gdoc(conf.PATH_TO_CRED)


def add_error(error_log):
    kp_errors.append(error_log)


def get_parser_instance(
    parser, locality=None, cnct_type=None, habitation=None, coordinates=None
):
    try:
        parserInst = parser.trf_parser(
            locality=locality,
            cnct_type=cnct_type,
            habitation=habitation,
            coordinates=coordinates,
        )
        if Parser in parserInst.__class__.__mro__:
            return parserInst
        else:
            add_error(
                f'Парсер "{parser.__name__}" Error "parserInst is not Parser-class"'
            )
    except Exception as e:
        add_error(f'Парсер "{parser.__name__}" вернул ошибку: {e}')


def write_to_gdoc(parserInst):
    gdocInst.g_sheets_update(parserInst, conf.KP_GDOC)


def main():

    # Mytelecom
    mytelecom_inst = get_parser_instance(mytelecom, habitation="aprtmnt")
    write_to_gdoc(mytelecom_inst) if mytelecom_inst else print(
        f"{mytelecom.__name__} Error"
    )
    mytelecom_inst = get_parser_instance(mytelecom, habitation="house")
    write_to_gdoc(mytelecom_inst) if mytelecom_inst else print(
        f"{mytelecom.__name__} Error"
    )

    # VIVA
    viva_inst = get_parser_instance(viva, habitation="aprtmnt")
    write_to_gdoc(viva_inst) if viva_inst else print(f"{viva.__name__} Error")

    # Prostor
    prostor_inst = get_parser_instance(prostor, cnct_type="wi-fi")
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")
    prostor_inst = get_parser_instance(prostor, cnct_type="cabel")
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Erema
    erema_inst = get_parser_instance(erema, cnct_type="cabel")
    write_to_gdoc(erema_inst) if erema_inst else print(f"{erema.__name__} Error")

    # Kyivstar
    kyivstar_inst = get_parser_instance(kyivstar, cnct_type="cabel")
    write_to_gdoc(kyivstar_inst) if kyivstar_inst else print(
        f"{kyivstar.__name__} Error"
    )

    # Ukrtelecom - Купянск
    ukrtelecom_inst = get_parser_instance(
        ukrtelecom, coordinates=[1363, 1384, 10639, "Купянск"]
    )
    write_to_gdoc(ukrtelecom_inst) if ukrtelecom_inst else print(
        f"{ukrtelecom.__name__} Error"
    )

    # Ukrtelecom - Купянск-Узловой
    ukrtelecom_inst = get_parser_instance(
        ukrtelecom, coordinates=[1363, 1384, 10640, "Купянск-Узловой"]
    )
    write_to_gdoc(ukrtelecom_inst) if ukrtelecom_inst else print(
        f"{ukrtelecom.__name__} Error"
    )

    # Ukrtelecom - Ковшаровка
    ukrtelecom_inst = get_parser_instance(
        ukrtelecom, coordinates=[1363, 1384, 10625, "Ковшаровка"]
    )
    write_to_gdoc(ukrtelecom_inst) if ukrtelecom_inst else print(
        f"{ukrtelecom.__name__} Error"
    )

    # Ukrtelecom - Подолы
    ukrtelecom_inst = get_parser_instance(
        ukrtelecom, coordinates=[1363, 1384, 14265, "Подолы"]
    )
    write_to_gdoc(ukrtelecom_inst) if ukrtelecom_inst else print(
        f"{ukrtelecom.__name__} Error"
    )

    # Ukrtelecom - Петропавловка
    ukrtelecom_inst = get_parser_instance(
        ukrtelecom, coordinates=[938, 960, 9168, "Петропавловка"]
    )
    write_to_gdoc(ukrtelecom_inst) if ukrtelecom_inst else print(
        f"{ukrtelecom.__name__} Error"
    )

    # Ukrtelecom - Куриловка
    ukrtelecom_inst = get_parser_instance(
        ukrtelecom, coordinates=[938, 959, 12412, "Куриловка"]
    )
    write_to_gdoc(ukrtelecom_inst) if ukrtelecom_inst else print(
        f"{ukrtelecom.__name__} Error"
    )

    # Ukrtelecom - Куриловка
    kupmytelecom_inst = get_parser_instance(kupmytelecom)
    write_to_gdoc(kupmytelecom_inst) if kupmytelecom_inst else print(
        f"{kupmytelecom.__name__} Error"
    )

    gdocInst.g_sheets_errorlog(kp_errors, conf.KP_GDOC)
