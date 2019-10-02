import conf

from parser.parser import Parser, DinamicParser
from gdoc.gdoc import Gdoc

import parser.bd.atv_plus as atv_plus
import parser.bd.flycom as flycom
import parser.bd.bel_net as bel_net
import parser.bd.kyivstar as kyivstar

bd_errors = []
gdocInst = Gdoc(conf.PATH_TO_CRED)


def add_error(error_log):
    bd_errors.append(error_log)


def get_parser_instance(parser, locality=None, cnct_type=None):
    try:
        parserInst = parser.trf_parser(locality=locality, cnct_type=cnct_type)
        if isinstance(parserInst, Parser) or isinstance(parserInst, DinamicParser):
            return parserInst
        else:
            add_error(
                f'Парсер "{parser.__name__}" Error "parserInst is not Parser-class"'
            )
    except Exception as e:
        add_error(f'Парсер "{parser.__name__}" вернул ошибку: {e}')


def write_to_gdoc(parserInst):
    gdocInst.g_sheets_update(parserInst, conf.BD_GDOC)


def main():

    # АТВ+
    atv_plus_inst = get_parser_instance(atv_plus)
    write_to_gdoc(atv_plus_inst) if atv_plus_inst else print(
        f"{atv_plus.__name__} Error"
    )

    # Flycom
    lcl_one = "sadovoe"
    lcl_two = "mologa"
    lcl_three = "vipasnoe"  # Only wi-fi
    lcl_four = "suholuzhie"  # Only wi-fi
    flycom_inst = get_parser_instance(flycom, lcl_one, "cabel")
    write_to_gdoc(flycom_inst) if flycom_inst else print(f"{flycom.__name__} Error")
    flycom_inst = get_parser_instance(flycom, lcl_one, "wi-fi")
    write_to_gdoc(flycom_inst) if flycom_inst else print(f"{flycom.__name__} Error")
    flycom_inst = get_parser_instance(flycom, lcl_two, "cabel")
    write_to_gdoc(flycom_inst) if flycom_inst else print(f"{flycom.__name__} Error")
    flycom_inst = get_parser_instance(flycom, lcl_two, "wi-fi")
    write_to_gdoc(flycom_inst) if flycom_inst else print(f"{flycom.__name__} Error")
    flycom_inst = get_parser_instance(flycom, lcl_three, "wi-fi")
    write_to_gdoc(flycom_inst) if flycom_inst else print(f"{flycom.__name__} Error")
    flycom_inst = get_parser_instance(flycom, lcl_four, "wi-fi")
    write_to_gdoc(flycom_inst) if flycom_inst else print(f"{flycom.__name__} Error")

    # Bel.net.ua
    bel_net_inst = get_parser_instance(bel_net, cnct_type="wi-fi")
    write_to_gdoc(bel_net_inst) if bel_net_inst else print(f"{bel_net.__name__} Error")

    # Kyivstar
    kyivstar_inst = get_parser_instance(kyivstar)
    write_to_gdoc(kyivstar_inst) if kyivstar_inst else print(
        f"{kyivstar.__name__} Error"
    )

    gdocInst.g_sheets_errorlog(bd_errors, conf.BD_GDOC)
