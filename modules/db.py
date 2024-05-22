#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import pymysql.connections
import pymysql.cursors
import os
############static variables#####################

#################################################


class DB:
    def __init__(self, config):
        super(DB, self).__init__()
        self.__config = config
        self.__cursor = None
        self.__db = None
        self.init()

    def init(self):
        self.__db = pymysql.connect(
                         host=self.__config.get_config()['db_host'],
                         user=self.__config.get_config()['db_login'],
                         password=self.__config.get_config()['db_password'],
                         database=self.__config.get_config()['db_schema'],
                         cursorclass=pymysql.cursors.DictCursor)
        self.__cursor = self.__db.cursor()
        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications(
            row_id BIGINT unsigned PRIMARY KEY,
            date_creation DATETIME,
            date_change DATETIME,
            transport_type TEXT,
            cargo_weight FLOAT,
            cargo_volume FLOAT,
            city_source TEXT,
            city_target TEXT,
            city_addition_source TEXT,
            city_addition_target TEXT,
            cargo_type TEXT,
            tags TEXT,
            company_name TEXT,
            company_link TEXT,
            worker_creds TEXT,
            phone_number TEXT,
            phone_number_whatsapp TEXT,
            email TEXT,
            price INT,
            tags_payment TEXT,
            status TEXT
        )
        ''')

    def db_write(self, queri, args):
        self.__cursor.execute(queri, args)
        self.__db.commit()

    def db_read(self, queri, args):
        self.__cursor.execute(queri, args)
        return self.__cursor.fetchall()