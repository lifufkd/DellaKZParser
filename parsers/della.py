#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import threading
import time
from seleniumbase import Driver
from datetime import datetime
from selenium.webdriver.common.by import By
from modules.CRUD import CRUD

############static variables#####################
#################################################


class Della:
    def __init__(self, db, url):
        super(Della, self).__init__()
        self.__driver = None
        self.__url = url
        self.__crud = CRUD(db)
        self.init()

    def init(self):
        self.__driver = Driver(ad_block_on=True, uc=True, headless=True, headless2=True, headed=False)

    def main(self):
        page = 0
        page_multiplayer = 100
        while True:
            actual_url = self.__url + f'r{page*page_multiplayer}l100.html'
            self.__driver.get(actual_url)
            page += 1
            time.sleep(3)
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            cards = self.__driver.find_elements(By.ID, 'request_list_main')[0].find_elements(By.TAG_NAME, 'div')
            for card in cards:
                print('-'*50)
                print(card.text)
                print('-' * 50)
            break

    def __del__(self):
        self.__driver.quit()
