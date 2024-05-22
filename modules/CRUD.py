#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import copy
import datetime
import json
############static variables#####################
#################################################


class CRUD:
    def __init__(self, db):
        super(CRUD, self).__init__()
        self.__db = db

    def add_application(self, data):
        self.__db.db_write('INSERT INTO applications (row_id, date_creation, date_change, transport_type, cargo_weight, '
                           'cargo_volume, city_source, city_addition_source, city_target, city_addition_target, '
                           'cargo_type, tags, company_name, company_link, worker_creds, phone_number, '
                           'phone_number_whatsapp, email, price, tags_payment, status) VALUES (%s, %s, %s, %s, %s, %s, '
                           '%s, %s'
                           ', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)

    def check_already_existed(self, row_id):
        data = self.__db.db_read('SELECT COUNT(*) FROM applications WHERE row_id = %s', (row_id, ))
        if len(data) > 0:
            if data[0]['COUNT(*)'] > 0:
                return True