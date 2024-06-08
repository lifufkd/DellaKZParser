#################################################
#                 created by                    #
#                     SBR                       #
#################################################
import os
import threading
import time
import logging
import datetime
from parsers.della import Della
from parsers.fa_fa import FaFa
from parsers.config_parser import ConfigParser
from modules.db import DB
############static variables#####################
config_name = 'secrets.json'
accounts_name_della = 'della_accounts.json'
accounts_name_fafa = 'fafa_accounts.json'
#################################################


def checker_fafa(timeout):
    while True:
        if (not 0 <= datetime.today().hour+config.get_config()['timezone'] <= 6) or not config.get_config()['enable_night_idle']:
            status = fafa.main()
            if status:
                time.sleep(timeout)
        else:
            time.sleep(1)


def checker_della(timeout):
    while True:
        if (not 0 <= datetime.today().hour+config.get_config()['timezone'] <= 6) or not config.get_config()['enable_night_idle']:
            status = della_kz.main()
            if status:
                time.sleep(timeout)
        else:
            time.sleep(1)


if __name__ == '__main__':
    work_dir = os.path.dirname(os.path.realpath(__file__))
    logger = logging.getLogger(__name__)
    config = ConfigParser(config_name, accounts_name_della, accounts_name_fafa)
    logging.basicConfig(filename=config.get_config()['log_file'], level=logging.INFO,)
    db = DB(config)
    #della_kz = Della(db, config, logger)
    fafa = FaFa(db, config, logger)
    # #threading.Thread(target=checker_della, args=(config.get_config()['timeout'], )).start()
    threading.Thread(target=checker_fafa, args=(config.get_config()['timeout'],)).start()