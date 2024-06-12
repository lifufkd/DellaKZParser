#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from datetime import datetime, timedelta
############static variables#####################
#################################################


class CRUD:
    def __init__(self, db, config):
        super(CRUD, self).__init__()
        self.__db = db
        self.__config = config

    def add_application(self, data):
        self.__db.db_write('INSERT INTO applications (row_id, date_creation, date_change, transport_type, cargo_weight, '
                           'cargo_volume, city_source, city_addition_source, city_target, city_addition_target, '
                           'cargo_type, cargo_addition, tags, company_name, company_link, worker_creds, phone_number, '
                           'phone_number_whatsapp, email, price, tags_payment, status) VALUES (%s, %s, %s, %s, %s, %s, '
                           '%s, %s'
                           ', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)

    def add_or_update_application(self, data):
        current_time = datetime.now().replace(microsecond=0)+timedelta(hours=self.__config.get_config()["timezone"])
        if not self.check_already_existed(data[0]):
            self.__db.db_write('INSERT INTO applications (created_at, updated_at, row_id, date_of_loading, date_creation, date_change, transport_type, cargo_weight, '
                               'cargo_volume, city_source, city_target, city_addition_source, city_addition_target, '
                               'cargo_type, cargo_addition, tags, company_name, company_link, worker_creds, phone_number, '
                               f'phone_number_whatsapp, email, price, tags_payment, processed) VALUES ("{current_time}", "{current_time}", %s, %s, %s, %s, '
                               '%s, %s'
                               ', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)
        else:
            self.__db.db_write(
                f'UPDATE applications SET updated_at = "{current_time}", date_of_loading = %s, date_creation = %s, date_change = %s, transport_type = %s, cargo_weight = %s, '
                'cargo_volume = %s, city_source = %s, city_target = %s, city_addition_source = %s, city_addition_target = %s, '
                'cargo_type = %s, cargo_addition = %s, tags = %s, company_name = %s, company_link = %s, worker_creds = %s, phone_number = %s, '
                f'phone_number_whatsapp = %s, email = %s, price = %s, tags_payment = %s, processed = %s WHERE row_id = {data[0]}', data[1:])

    def check_already_existed(self, row_id):
        data = self.__db.db_read('SELECT COUNT(*) FROM applications WHERE row_id = %s', (row_id, ))
        if len(data) > 0:
            if data[0]['COUNT(*)'] > 0:
                return True

    def get_status(self, row_id):
        return self.__db.db_read('SELECT status FROM applications WHERE row_id = %s', (row_id, ))[0]['status']

    def update_application(self, row_id, new_status):
        if self.get_status(row_id) != new_status:
            self.__db.db_write('UPDATE applications SET status = %s WHERE row_id = %s', (new_status, row_id))
            return True