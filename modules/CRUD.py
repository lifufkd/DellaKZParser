#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import copy
import json
############static variables#####################
#################################################


class CRUD:
    def __init__(self, db):
        super(CRUD, self).__init__()
        self.__db = db

    def add_apartment(self, data):
        print(data)
        self.__db.db_write(f'INSERT INTO appartaments (link, address, floor, square, rooms, price, date, source, comments) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "{json.dumps([])}")', data)

    def get_existed_apartment(self, url):
        data = self.__db.db_read('SELECT COUNT(*) FROM appartaments WHERE link = ?', (url, ))[0][0]
        print(data)
        if data == 0:
            return True

    def get_all_count_apartments(self):
        return self.__db.db_read('SELECT COUNT(*) FROM appartaments', ())[0][0]

    def check_login(self, login, password):
        data = self.__db.db_read('SELECT COUNT(*) FROM users WHERE login = ? AND password = ?', (login, password))[0][0]
        if data > 0:
            return True

    def add_user(self, data):
        self.__db.db_write('INSERT INTO users (name, lastname, email, login, password) VALUES (?, ?, ?, ?, ?)', data)

    def get_basic_query(self):
        return self.__db.db_read('SELECT row_id, link, address, floor, square, rooms, price, date, source FROM appartaments LIMIT 10', ())

    def get_restricted_query(self, restrictions):
        print(restrictions)
        apartments = self.__db.db_read(
            'SELECT row_id, link, address, floor, square, rooms, price, date, source FROM appartaments', ())
        for index, rests in enumerate(restrictions):
            if rests:
                temp = list()
                match index:
                    case 0:
                        for i in apartments:
                            if i[5] == rests:
                                temp.append(i)
                        apartments = copy.deepcopy(temp)
                    case 2:
                        for i in apartments:
                            if rests.lower() in i[2].lower():
                                temp.append(i)
                        apartments = copy.deepcopy(temp)
                    case 3:
                        for i in apartments:
                            try:
                                square = int(i[4][:i[4].find(' ')])
                                if rests == square:
                                    temp.append(i)
                            except:
                                pass
                        apartments = copy.deepcopy(temp)
                    case 4:
                        for i in apartments:
                            try:
                                price = int(i[6][:i[6].find('₽')-1].replace(" ", ""))
                                if rests == price:
                                    temp.append(i)
                            except:
                                pass
                        apartments = copy.deepcopy(temp)
                    case 5:
                        for i in apartments:
                            try:
                                price = int(i[3][:i[3].find('из') - 1])
                                if rests == price:
                                    temp.append(i)
                            except:
                                pass
                        apartments = copy.deepcopy(temp)
        return apartments[:10]

    def get_comments_by_id(self, row_id):
        return json.loads(self.__db.db_read('SELECT comments FROM appartaments WHERE row_id = ?', (row_id, ))[0][0])

    def add_comment_by_id(self, row_id, comment, creds):
        data = self.get_comments_by_id(row_id)
        user_data = self.__db.db_read(f'SELECT name, lastname FROM users WHERE login = "{creds[0]}" AND password = "{creds[1]}"', ())[0]
        data.append(f'{user_data[0]} {user_data[1]} > {comment}')
        self.__db.db_write('UPDATE appartaments SET comments = ? WHERE row_id = ?', (json.dumps(data), row_id))