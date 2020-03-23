import conf

from parser.parser import Parser, DinamicParser
from gdoc.gdoc import Gdoc

import parser.mg.stcom as stcom
import parser.mg.kyivstarfmc as kyivstarfmc
import parser.mg.prostor as prostor

bd_errors = []
gdocInst = Gdoc(conf.PATH_TO_CRED)


def add_error(error_log):
    bd_errors.append(error_log)


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
    gdocInst.g_sheets_update(parserInst, conf.MG_GDOC)


def main():

    # Prostor/STcom - Марганец
    prostor_inst = get_parser_instance(prostor, cnct_type="cabel", locality="Марганец")
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Kyivstar-fmc
    kyivstarfmc_inst = get_parser_instance(kyivstarfmc)
    write_to_gdoc(kyivstarfmc_inst) if kyivstarfmc_inst else print(
        f"{kyivstarfmc.__name__} Error"
    )

    # Prostor - Городище - cabel
    prostor_inst = get_parser_instance(prostor, cnct_type="cabel", locality="Городище")
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Prostor - Городище - wi-fi
    prostor_inst = get_parser_instance(prostor, cnct_type="wi-fi", locality="Городище")
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Prostor - Закамянка - cabel
    prostor_inst = get_parser_instance(prostor, cnct_type="cabel", locality="Закамянка")
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Prostor - Закамянка - wi-fi
    prostor_inst = get_parser_instance(prostor, cnct_type="wi-fi", locality="Закамянка")
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Prostor - Максимівка - cabel
    prostor_inst = get_parser_instance(
        prostor, cnct_type="cabel", locality="Максимівка"
    )
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Prostor - Максимівка - wi-fi
    prostor_inst = get_parser_instance(
        prostor, cnct_type="wi-fi", locality="Максимівка"
    )
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Prostor - Марьивка - cabel
    prostor_inst = get_parser_instance(prostor, cnct_type="cabel", locality="Марьивка")
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Prostor - Новоселовка - cabel
    prostor_inst = get_parser_instance(
        prostor, cnct_type="cabel", locality="Новоселівка"
    )
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    # Prostor - Остров - cabel
    prostor_inst = get_parser_instance(prostor, cnct_type="cabel", locality="Остров")
    write_to_gdoc(prostor_inst) if prostor_inst else print(f"{prostor.__name__} Error")

    gdocInst.g_sheets_errorlog(bd_errors, conf.MG_GDOC)
