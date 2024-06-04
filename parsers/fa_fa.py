#################################################
#                 created by                    #
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


class FaFa:
    def __init__(self, db, config, logger):
        super(FaFa, self).__init__()
        self.__driver = None
        self.__config = config
        self.__logger = logger
        self.__cards_parsed = 0
        self.__creds_index = 0
        self.__elements = [
            ['date_ins', By.CLASS_NAME],
            ['date_up', By.CLASS_NAME],
            ['truck_type', By.CLASS_NAME],
            ['weight', By.CLASS_NAME],
            ['cube', By.CLASS_NAME],
            ['request_route', By.CLASS_NAME],
            ['request_text', 'cargo_type', By.CLASS_NAME],
            ['request_tags', By.CLASS_NAME, 'tag'],
            ['company_link', By.CLASS_NAME],
            ['contact_name', By.CLASS_NAME],
            ['phones', 'whatsapp', 'email', By.CLASS_NAME],
            ['price_main', By.CLASS_NAME],
            ['price_tags', By.CLASS_NAME, 'tag'],
            ['new', 'closed', By.CLASS_NAME]]
        self.__crud = CRUD(db)
        self.init()

    def init(self):
        # , headless2=True, headed=False, agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        self.__driver = Driver(ad_block_on=True, uc=True, no_sandbox=True, proxy="proxy1", uc_cdp=True,
                               uc_cdp_events=True)
        self.__driver.get(self.__config.get_config()['fafa_home_page'])
        self.log_in(self.__config.get_accounts_config_fafa())

    def error_parse(self, output, quanity=1):
        for g in range(quanity):
            output.append(None)

    def log_in(self, creds):
        while True:
            try:
                self.__driver.find_element(By.CSS_SELECTOR, 'div#header1 > table > tbody > tr > td > table > tbody > tr:nth-of-type(2) > td:nth-of-type(4) > table > tbody > tr > td:nth-of-type(4) > form > input:nth-of-type(2)').send_keys(creds[self.__creds_index][0])
                time.sleep(random.random() * 5)
                self.__driver.find_element(By.CSS_SELECTOR, 'input#f_pass').send_keys(creds[self.__creds_index][1])
                time.sleep(random.random() * 2)
                self.__driver.find_element(By.CSS_SELECTOR, 'div#header1 > table > tbody > tr > td > table > tbody > tr:nth-of-type(2) > td:nth-of-type(4) > table > tbody > tr > td:nth-of-type(4) > form > input:nth-of-type(4)').click()
                time.sleep(random.random() * 2)
                break
            except Exception as e:
                print(e)
                time.sleep(3)

    def log_out(self):
        c = 0
        while True:
            try:
                c += 1
                self.__driver.find_element(By.CSS_SELECTOR, 'div#header1 > table > tbody > tr > td > table > tbody > tr:nth-of-type(2) > td:nth-of-type(4) > table > tbody > tr > td > a').click()
                time.sleep(random.random() * 3)
                break
            except:
                time.sleep(3)
            if c >= 5:
                break

    def close_sign_up_menu(self):
        try:
            self.__driver.find_element(By.CSS_SELECTOR, 'div#signupmwnd > div:nth-of-type(2) > img').click()
        except:
            pass

    def recheck_card(self, card_id, card_obj):
        flag = False
        for i in range(2):
            try:
                data = card_obj.find_element(self.__elements[13][2], self.__elements[13][i]).text
                flag = True
                break
            except:
                pass
        if flag:
            return self.__crud.update_application(card_id[8:], data)

    def parse_card(self, card_id, card_obj):
        output = [card_id[8:]]
        for index, element in enumerate(self.__elements):
            try:
                if index == 10:
                    data = [card_obj.find_elements(element[3], element[0]),
                            card_obj.find_elements(element[3], element[1]),
                            card_obj.find_elements(element[3], element[2])]
                elif index == 8:
                    company_data = card_obj.find_element(element[1], element[0])
                    data = [company_data.text, company_data.get_attribute('href')]
                elif index == 6:
                    data = [card_obj.find_element(element[2], element[0]).text,
                            card_obj.find_element(element[2], element[1]).text]
                elif index in [7, 12]:
                    data = card_obj.find_element(element[1], element[0]).find_elements(element[1], element[2])
                elif index == 13:
                    pass
                else:
                    data = card_obj.find_element(element[1], element[0]).text
            except:
                match index:
                    case 10:
                        self.error_parse(output, 3)
                    case 8:
                        self.error_parse(output, 2)
                    case 5:
                        self.error_parse(output, 4)
                    case 6:
                        self.error_parse(output, 2)
                    case _:
                        self.error_parse(output)
                continue
            if index in range(2):
                try:
                    date = data[data.index('.') + 2:]
                    formated_date = date[:5] + f'.{datetime.now().year}' + date[5:]
                    date_time_obj = datetime.strptime(formated_date, "%d.%m.%Y %H:%M")
                    output.append(date_time_obj)
                except:
                    self.error_parse(output)
            elif index == 6:
                print(f'{data} CARGO')
                try:
                    temp = list()
                    start = 0
                    addition = data[0].replace(data[1], '').strip() + '  '
                    if ' ' in addition:
                        for indexx, i in enumerate(addition):
                            if i == ' ' and addition[indexx - 1] not in ['.', ':', ',']:
                                if len(addition[start:indexx]) > 0:
                                    temp.append(addition[start:indexx])
                                start = indexx + 1
                    else:
                        temp.append(addition)
                    output.extend([data[1], json.dumps(temp)])
                except:
                    self.error_parse(output, 2)
            elif index in [2, 9]:
                output.append(data)
            elif index in [3, 4]:
                flag = False
                for i in [' т', ' м³']:
                    try:
                        if '-' in data:
                            t_index = data.index('-')
                            output.append(float(data[t_index + 1:data.index(i)].replace(',', '.')))
                        else:
                            output.append(float(data[:data.index(i)].replace(',', '.')))
                        flag = True
                        break
                    except:
                        pass
                if not flag:
                    self.error_parse(output)
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
                    self.error_parse(output, 4)
            # tags
            elif index in [7, 12]:
                temp = list()
                try:
                    for i in data:
                        temp.append(i.text)
                    output.append(json.dumps(temp))
                except:
                    self.error_parse(output)
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
                        self.error_parse(output)
            elif index == 11:
                try:
                    data = data.replace('\n', '')
                    data = data[:data.index(' тнг')].replace(' ', '')
                    output.append(int(data))
                except:
                    self.error_parse(output)
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
                    self.error_parse(output)
        self.__logger.info(output)
        try:
            self.__crud.add_application(output)
        except:
            pass

    def main(self) -> False or True:
        actual_url = self.__config.get_config()['fafa_url']
        self.__driver.get(actual_url)
        time.sleep(5)
        cards = self.__driver.find_element(By.CSS_SELECTOR, 'div#request_list_main').find_elements(By.XPATH, "./*")
        for card in cards:
            card_id = card.get_attribute('id')
            if card_id[:7] == "request":
                if self.__cards_parsed >= self.__config.get_config()['change_account_cards_limit'] and len(
                        self.__config.get_accounts_config_fafa()) > 1:
                    self.__cards_parsed = 0
                    if len(self.__config.get_accounts_config_fafa()) - 1 >= self.__creds_index:
                        self.__creds_index = 0
                    else:
                        self.__creds_index += 1
                    # self.close_sign_up_menu()
                    # time.sleep(random.random() * 3)
                    self.log_out()
                    time.sleep(5)
                    self.log_in(self.__config.get_accounts_config_fafa())
                    return False
                if self.__crud.check_already_existed(int(card_id[8:])):
                    if self.recheck_card(card_id, card):
                        continue
                    else:
                        return True
                else:
                    try:
                        button = card.find_element(By.CLASS_NAME, 'show_request_info_btn')
                        self.__driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(1)
                        button.click()
                    except:
                        self.__logger.info('button_dont_click')
                    finally:
                        time.sleep(self.__config.get_config()['timeout_cards_btn'])
                        self.parse_card(card_id, card)
                self.__cards_parsed += 1

    def __del__(self):
        self.__driver.quit()
