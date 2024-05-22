#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
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
        def error_parse():
            output.append(None)
        output = [card_id]
        elements = [
            ['date_ins', By.CLASS_NAME],
            ['date_up', By.CLASS_NAME],
            ['truck_type', By.CLASS_NAME],
            ['weight', By.CLASS_NAME],
            ['cube', By.CLASS_NAME],
            ['request_route', By.CLASS_NAME],
            ['cargo_type', By.CLASS_NAME],
            ['request_tags', By.CLASS_NAME],
            ['company_link', By.CLASS_NAME],
            ['contact_name', By.CLASS_NAME],
            ['value', By.CLASS_NAME],
            ['price_main', By.CLASS_NAME],
            ['price_tags', By.CLASS_NAME]]
        for index, element in enumerate(elements):
            data = None
            try:
                if index == 10:
                    data = card_obj.find_elements(element[1], element[0])
                elif index == 8:
                    company_data = card_obj.find_element(element[1], element[0])
                    data = [company_data.text, company_data.get_attribute('href')]
                else:
                    data = card_obj.find_element(element[1], element[0]).text
            except:
                error_parse()
                continue
            if index in range(2):
                try:
                    date = data[data.index('.')+2]
                    formated_date = date[:5] + datetime.now().year + date[index:5]
                    date_time_obj = datetime.strptime(formated_date, "%d.%m.%y %H:%M")
                    print(date_time_obj)
                    output.append(date_time_obj)
                except:
                    print('error_dates')
                    error_parse()
            elif index in [2, 6, 9]:
                output.append(data)
            elif index in [3, 4]:
                try:
                    output.append(float(data))
                except:
                    print('error_float')
                    error_parse()
            elif index == 5:
                output = list()
                cities = data[:data.index('~') - 2]
                source_cities = cities[:cities.index('—') - 1]
                destination_cities = cities[cities.index('—') + 2:]
                first = True
                for i in source_cities.split(','):
                    if first:
                        output.extend([i.strip(), []])
                        first = False
                    else:
                        output[-1].append(i.strip())
                first = True
                for i in destination_cities.split(','):
                    if first:
                        output.extend([i.strip(), []])
                        first = False
                    else:
                        output[-1].append(i.strip())
            # tags
            elif index in [7, 12]:
                pass
            elif index in [8]:
                output.extend(data)
            elif index == 10:
                for i in range(3):
                    try:
                        output.append(data[i].text)
                    except:
                        error_parse()
            elif index == 11:
                pass

    def main(self):
        page = 0
        page_multiplayer = 100
        self.log_in()
        while True:
            actual_url = self.__config.get_config()['url'] + f'r{page*page_multiplayer}l100.html'
            self.__driver.get(actual_url)
            time.sleep(10)
            # self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(10)
            cards = self.__driver.find_element(By.CSS_SELECTOR, 'div#request_list_main').find_elements(By.XPATH, "./*")
            print(cards)
            for card in cards:
                card_id = card.get_attribute('id')
                if card_id[:7] == "request":
                    try:
                        card.find_element(By.TAG_NAME, 'button').click()
                        time.sleep(3)
                    except Exception as e:
                        print(e)
                    finally:
                        self.parse_card(card_id, card)
                break
            page += 1
            break

    def __del__(self):
        self.__driver.quit()
