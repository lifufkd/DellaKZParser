#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import os
import threading
import time
import logging
from parsers.della import Della
from parsers.config_parser import ConfigParser
from modules.db import DB
############static variables#####################
config_name = 'secrets.json'
#################################################


def checker(timeout):
    while True:
        della_kz.main()
        time.sleep(timeout)


if __name__ == '__main__':
    work_dir = os.path.dirname(os.path.realpath(__file__))
    logger = logging.getLogger(__name__)
    config = ConfigParser(config_name)
    logging.basicConfig(filename=config.get_config()['log_file'], level=logging.INFO)
    db = DB(config)
    della_kz = Della(db, config, logger)
    threading.Thread(target=checker, args=(config.get_config()['timeout'], )).start()