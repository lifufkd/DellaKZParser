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

    def parse_card(self, card_id):
        def error_parse():
            print('error')
            output.append(None)
        output = [card_id]
        elements = [
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(2) > div > div:nth-of-type(2),'
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(2) > div > div',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(2) > div > div > div:nth-of-type(2) > div:nth-of-type(2)',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(2) > div > div > div:nth-of-type(3) > div:nth-of-type(2)',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(2) > div > div > div:nth-of-type(4) > div:nth-of-type(2)',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2)',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(3) > div > span',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(3) > div:nth-of-type(2)',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(3) > div > div > div:nth-of-type(2) > div > a',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(3) > div > div > div:nth-of-type(3)',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(3) > div > div > div:nth-of-type(4) > div > div > a',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(3) > div > div > div:nth-of-type(3) > div:nth-of-type(3) > div > a',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(3) > div > div > div:nth-of-type(3) > div:nth-of-type(2) > div > a',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div > div',
            f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(3)']
        for index, element in enumerate(elements):
            try:
                data = self.__driver.find_element(By.CSS_SELECTOR, element).text
            except:
                error_parse()
                continue
            print(data)
            if index in range(2):
                try:
                    date = data[data.index('.')+2]
                    formated_date = date[:5] + datetime.now().year + date[index:5]
                    date_time_obj = datetime.strptime(formated_date, "%d.%m.%y %H:%M")
                    print(date_time_obj)
                    output.append(date_time_obj)
                except:
                    error_parse()
            elif index in [2]:
                output.append(data)
            elif index in [3, 4]:
                try:
                    output.append(float(data))
                except:
                    error_parse()

    def main(self):
        page = 0
        page_multiplayer = 100
        self.log_in()
        while True:
            actual_url = self.__config.get_config()['url'] + f'r{page*page_multiplayer}l100.html'
            self.__driver.get(actual_url)
            page += 1
            time.sleep(3)
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            cards = self.__driver.find_element(By.CSS_SELECTOR, 'div#request_list_main').find_elements(By.XPATH, "./*")
            print(cards)
            for card in cards:
                card_id = card.get_attribute('id')
                if card_id[:7] == "request":
                    try:
                        self.__driver.find_element(By.CSS_SELECTOR, f'div#{card_id} > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > button').click()
                        time.sleep(1)
                    except:
                        pass
                    finally:
                        self.parse_card(card_id)
            break

    def __del__(self):
        self.__driver.quit()
