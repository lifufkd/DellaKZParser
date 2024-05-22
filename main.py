#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import os
from parsers.della import Della
from parsers.config_parser import ConfigParser
from modules.CRUD import CRUD
from modules.db import DB
############static variables#####################
config_name = 'secrets.json'
#################################################

if __name__ == '__main__':
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(config_name)
    db = DB(config)
    della_kz = Della(db, config)
    della_kz.main()