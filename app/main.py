import conf

from time import sleep

from gdoc.gdoc import Gdoc
from parser.bd.bd_handler import main as bd
from parser.kp.kp_handler import main as kp
from parser.mg.mg_handler import main as mg
from parser.od.od_handler import main as od

delay = 100

def index():

    gdocInst = Gdoc(conf.PATH_TO_CRED)

    gdocInst.add_colums(conf.BD_GDOC)
    bd()
    print('BD tarifs parsed')
    sleep(delay)
    gdocInst.add_colums(conf.KP_GDOC)
    kp()
    print('KP tarifs parsed')
    sleep(delay)
    gdocInst.add_colums(conf.MG_GDOC)
    mg()
    print('MG tarifs parsed')
    sleep(delay)
    gdocInst.add_colums(conf.OD_GDOC)
    od()
    print('OD tarifs parsed')

index()