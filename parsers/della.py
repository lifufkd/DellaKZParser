#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import json
import threading
import time
import random
from seleniumbase import Driver
from datetime import datetime
from selenium.webdriver.common.by import By
from modules.CRUD import CRUD

############static variables#####################
#################################################


class Della:
    def __init__(self, db, config):
        super(Della, self).__init__()
        self.__driver = None
        self.__config = config
        self.__crud = CRUD(db)
        self.init()

    def init(self):
        self.__driver = Driver(ad_block_on=True, uc=True)
        self.log_in()

    def log_in(self):
        self.__driver.get(self.__config.get_config()['home_page'])
        time.sleep(3)
        self.__driver.find_element(By.XPATH, '/html/body/table/tbody/tr[1]/td/table/tbody/tr[1]/td[3]/div[3]/div/div[1]').click()
        time.sleep(1)
        form = self.__driver.find_element(By.XPATH, '/html/body/div[6]/div/div[3]')
        time.sleep(random.random() * 3)
        form.find_element(By.ID, 'login').send_keys(self.__config.get_config()['account_login'])
        time.sleep(random.random() * 5)
        form.find_element(By.ID, 'password').send_keys(self.__config.get_config()['account_password'])
        time.sleep(random.random() * 2)
        form.find_elements(By.TAG_NAME, 'button')[1].click()

    def parse_card(self, card_id, card_obj):
        def error_parse(quanity=1):
            for g in range(quanity):
                output.append(None)
        output = [card_id[8:]]
        elements = [
            ['date_ins', By.CLASS_NAME],
            ['date_up', By.CLASS_NAME],
            ['truck_type', By.CLASS_NAME],
            ['weight', By.CLASS_NAME],
            ['cube', By.CLASS_NAME],
            ['request_route', By.CLASS_NAME],
            ['cargo_type', By.CLASS_NAME],
            ['request_tags', By.CLASS_NAME, 'tag'],
            ['company_link', By.CLASS_NAME],
            ['contact_name', By.CLASS_NAME],
            ['phones', 'whatsapp', 'email', By.CLASS_NAME],
            ['price_main', By.CLASS_NAME],
            ['price_tags', By.CLASS_NAME, 'tag'],
            ['new', 'closed', By.CLASS_NAME]]
        for index, element in enumerate(elements):
            try:
                if index == 10:
                    data = [card_obj.find_elements(element[3], element[0]), card_obj.find_elements(element[3], element[1]), card_obj.find_elements(element[3], element[2])]
                elif index == 8:
                    company_data = card_obj.find_element(element[1], element[0])
                    data = [company_data.text, company_data.get_attribute('href')]
                elif index in [7, 12]:
                    data = card_obj.find_element(element[1], element[0]).find_elements(element[1], element[2])
                elif index == 13:
                    pass
                else:
                    data = card_obj.find_element(element[1], element[0]).text
            except:
                match index:
                    case 10:
                        error_parse(3)
                    case 8:
                        error_parse(2)
                    case _:
                        error_parse()
                continue
            if index in range(2):
                try:
                    date = data[data.index('.')+2:]
                    formated_date = date[:5] + f'.{datetime.now().year}' + date[5:]
                    date_time_obj = datetime.strptime(formated_date, "%d.%m.%Y %H:%M")
                    output.append(date_time_obj)
                except:
                    error_parse()
            elif index in [2, 6, 9]:
                output.append(data)
            elif index in [3, 4]:
                flag = False
                for i in [' т', ' м³']:
                    try:
                        if '-' in data:
                            t_index = data.index('-')
                            output.append(float(data[t_index+1:data.index(i)].replace(',', '.')))
                        else:
                            output.append(float(data[:data.index(i)].replace(',', '.')))
                        flag = True
                        break
                    except:
                        pass
                if not flag:
                    error_parse()
            elif index == 5:
                temp = list()
                try:
                    if '~' in data:
                        cities = data[:data.index('~') - 2]
                    else:
                        cities = data
                    source_cities = cities[:cities.index('—') - 1]
                    destination_cities = cities[cities.index('—') + 2:]
                    first = True
                    for i in source_cities.split(','):
                        if first:
                            temp.extend([i.strip().replace(' (KZ)', ''), []])
                            first = False
                        else:
                            temp[-1].append(i.strip())
                    first = True
                    for i in destination_cities.split(','):
                        if first:
                            temp.extend([i.strip().replace(' (KZ)', ''), []])
                            first = False
                        else:
                            temp[-1].append(i.strip())
                    temp[1] = json.dumps(temp[1])
                    temp[3] = json.dumps(temp[3])
                    output.extend(temp)
                except:
                    error_parse(4)
            # tags
            elif index in [7, 12]:
                temp = list()
                for i in data:
                    temp.append(i.text)
                output.append(json.dumps(temp))
            elif index == 8:
                output.extend(data)
            elif index == 10:
                for indexx, i in enumerate(data):
                    try:
                        if indexx != 2:
                            phone = i[0].text[1:].replace('(', '').replace(')', '')
                            output.append(phone)
                        else:
                            output.append(i[0].text)
                    except:
                        error_parse()
            elif index == 11:
                try:
                    data = data.replace('\n', '')
                    data = data[:data.index(' тнг')].replace(' ', '')
                    output.append(int(data))
                except:
                    error_parse()
            elif index == 13:
                flag = False
                for i in range(2):
                    try:
                        data = card_obj.find_element(element[2], element[i]).text
                        flag = True
                        break
                    except:
                        pass
                if flag:
                    output.append(data)
                else:
                    error_parse()
        print(output)
        print(len(output))
        self.__crud.add_application(output)

    def main(self) -> None:
        page = 0
        page_multiplayer = 100
        while True:
            actual_url = self.__config.get_config()['url'] + f'r{page*page_multiplayer}l100.html'
            self.__driver.get(actual_url)
            time.sleep(5)
            # self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(10)
            cards = self.__driver.find_element(By.CSS_SELECTOR, 'div#request_list_main').find_elements(By.XPATH, "./*")
            for card in cards:
                card_id = card.get_attribute('id')
                if card_id[:7] == "request":
                    if self.__crud.check_already_existed(int(card_id[8:])):
                        print('111111')
                        return None
                    else:
                        try:
                            card.find_element(By.TAG_NAME, 'button').click()
                        except:
                            print('button_dont_click')
                        finally:
                            time.sleep(3)
                            self.parse_card(card_id, card)
            page += 1

    def __del__(self):
        self.__driver.quit()
