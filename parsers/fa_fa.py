#################################################
#                 created by                    #
#                     SBR                       #
#################################################
import json
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
            ['s_date2', By.CLASS_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME]]
        self.__buttons_ids = ['b_yes', 'b_no', 'b_unav', 'b_poh']
        self.__crud = CRUD(db, config)
        self.init()

    def parse_card(self, card_id, card_obj):
        output = [card_id]
        checker = 0
        for index, element in enumerate(self.__elements):
            try:
                if index == 0:
                    data = card_obj.find_element(element[1], element[0]).find_element(By.XPATH, './..').text
                elif index == 1:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[3].find_element(By.TAG_NAME, "b").text
                elif index == 2:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        4].find_element(By.TAG_NAME, "b").text
                elif index == 3:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        3].find_element(By.TAG_NAME, "a").text
                elif index == 4:
                    data = [card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        4].text, card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        3].text]
                elif index == 5:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        3].text
                elif index == 6:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        5].find_elements(By.TAG_NAME, "div")[0].find_element(By.TAG_NAME, "a")
                elif index == 7:
                    for i in range(2):
                        data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                            5].find_element(By.TAG_NAME, "td").find_elements(By.TAG_NAME, "div")[i+1].text
                        if len(data) != 0:
                            break
                elif index == 8:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        3].text
            except:
                match index:
                    case 0:
                        self.error_parse(output, 3)
                    case 1:
                        self.error_parse(output, 1)
                    case 2:
                        self.error_parse(output, 2)
                    case 3:
                        self.error_parse(output, 4)
                    case 4:
                        self.error_parse(output, 3)
                    case 5:
                        self.error_parse(output, 1)
                    case 6:
                        self.error_parse(output, 2)
                    case 7:
                        self.error_parse(output, 4)
                    case 8:
                        self.error_parse(output, 3)
                    case _:
                        self.error_parse(output)
                continue
            # Дата добавления и изменения
            if index == 0:
                monthes = {'января': "01", 'февраля': "02", 'марта': "03", 'апреля': "04", 'мая': "05", 'июня': "06",
                           'июля': "07", 'августа': "08", 'сентября': "09", 'октября': "10", 'ноября': "11", 'декабря': "12",}
                try:
                    data = data.split('\n')
                    output.extend([None, None, None])
                    if '-' in data[0]:
                        output[-3] = datetime.strptime(f'{data[0][:5]}.{datetime.now().year} 00:00', "%d.%m.%Y %H:%M")
                    else:
                        output[-3] =datetime.strptime(f'{data[0]}.{datetime.now().year} 00:00', "%d.%m.%Y %H:%M")
                    for i in range(2):
                        try:
                            if data[i+2][:4] == "изм.":
                                if ':' in data[i+2][6:]:
                                    formated_date = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year} {data[i+2][6:]}'
                                else:
                                    formated_date = f'{data[i+2][6:8]}.{monthes[data[i+2][9:]]}.{datetime.now().year} 00:00'
                                date_time_obj = datetime.strptime(formated_date, "%d.%m.%Y %H:%M")
                                output[-1] = date_time_obj
                            elif data[i+2][:4] == "доб.":
                                if ':' in data[i+2][6:]:
                                    formated_date = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year} {data[i+2][6:]}'
                                else:
                                    formated_date = f'{data[i+2][6:8]}.{monthes[data[i+2][9:]]}.{datetime.now().year} 00:00'
                                date_time_obj = datetime.strptime(formated_date, "%d.%m.%Y %H:%M")
                                output[-2] = date_time_obj
                        except:
                            pass
                except:
                    pass
            elif index == 1:
                output.append(data)
            elif index == 2:
                try:
                    data = data.split('/')
                    try:
                        weight = data[0][:-2]
                    except:
                        weight = None
                    try:
                        volume = data[1][1:-2]
                    except:
                        volume = None
                    if ',' in weight:
                        weight = weight.replace(',', '.')
                    elif ',' in volume:
                        volume = volume.replace(',', '.')
                    output.extend([float(weight), float(volume)])
                except:
                    self.error_parse(output, 2)
            elif index == 3:
                temp = []
                try:
                    if ' - ' in data:
                        cities = data[:data.index(' - ')]
                    else:
                        cities = data
                    cities = cities.split('→')
                    temp.append(cities[0].replace(', KZ', '')[:-1])
                    temp.append(cities[-1].replace(', KZ', '')[1:])
                    temp.extend([[], []])
                    if len(cities) > 2:
                        for el in cities[1:-1]:
                            if 'догр.' in el:
                                temp[2].append(el[7:].replace(', KZ', ''))
                            elif 'выгр.' in el:
                                temp[3].append(el[7:].replace(', KZ', ''))
                    temp[2] = json.dumps(temp[2])
                    temp[3] = json.dumps(temp[3])
                    output.extend(temp)
                except:
                    self.error_parse(output, 4)
            elif index == 4:
                try:
                    print(data)
                    cargo_addition = list()
                    comment = None
                    first_data = data[0].split('\n')
                    second_data = data[1].split('\n')
                    if ',' in first_data[1]:
                        cargo_type = first_data[1][:first_data[1].index(',')]
                        cargo_addition.append(first_data[1][first_data[1].index(',')+1:])
                    else:
                        cargo_type = first_data[1]
                    if len(second_data) > 1:
                        cargo_addition.append(second_data[1])
                        if len(cargo_addition) != 0:
                            for index, i in enumerate(cargo_addition):
                                cargo_addition[index] = i.replace('\n', ' ')
                        else:
                            cargo_addition = None
                    if len(second_data) > 2:
                        if 'тнг' not in second_data[2]:
                            comment = second_data[2]
                    output.extend([cargo_type, json.dumps(cargo_addition), comment])
                except:
                    self.error_parse(output, 3)
            elif index == 5:
                success = False
                try:
                    data = data.split('\n')[2:]
                    for i in data:
                        if i[0] == ' ':
                            success = True
                            output.append(i[1:])
                            break
                    if not success:
                        raise
                except:
                    self.error_parse(output)
            elif index == 6:
                try:
                    if 'частное лицо' in data.text.lower():
                        company_name = 'Частное лицо'
                    else:
                        company_name = data.text
                    output.extend([company_name, data.get_attribute('href')])
                except:
                    self.error_parse(output, 2)
            elif index == 7:
                temp = [None, None, None, None]
                try:
                    data = data.replace('\n', ' ')
                    if ':' in data:
                        temp[0] = data[:data.index(':')]
                        data = data[data.index(':')+2:].split(' ')
                    else:
                        data = data.split(' ')
                    for i in data:
                        if '+' in i:
                            temp[1] = i
                            temp[2] = i
                        elif '@' in i:
                            temp[3] = i
                    output.extend(temp)
                except:
                    self.error_parse(output, 4)
            elif index == 8:
                success = False
                output.extend([None, None, None])
                try:
                    data = data.split('\n')[2:]
                    for i in data:
                        if 'usd.' in i or 'руб.' in i or 'тнг.' in i:
                            sub = i.strip()
                            first_space_index = sub.index(' ')
                            second_space_index = sub.index(' ', first_space_index+1)
                            success = True
                            price = sub[:first_space_index]
                            tags = json.dumps([sub[second_space_index+1:]])
                            currency = sub[first_space_index+1:second_space_index-1]
                            if '.' in price:
                                price = price.replace('.', '')
                                output[-1] = tags
                                output[-2] = currency
                                output[-3] = price
                                break
                    if not success:
                        raise
                except:
                    pass
        self.__logger.info(output)
        try:
            output.append(0)
            for i in output:
                if i is None:
                    checker += 1
            if checker < 21:
                print(output)
                self.__crud.add_or_update_application(output)
        except Exception as e:
            print(e)

    def close_tab_by_domain(self, driver, domain_name):
        # Get the handle of the current window
        original_window = driver.current_window_handle

        # Get all window handles
        all_windows = driver.window_handles

        for window in all_windows:
            driver.switch_to.window(window)
            current_url = driver.current_url

            # Check if the current URL contains the domain name
            if domain_name in current_url:
                driver.close()
                break

        # Switch back to the original window
        driver.switch_to.window(original_window)

    def init(self):
        # product version
        self.__driver = Driver(uc=True, no_sandbox=True, proxy="proxy1", uc_cdp=True,
                               uc_cdp_events=True, extension_dir='./adblock', headless2=True, headed=False, agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36')
        time.sleep(20)
        # self.__driver = Driver(uc=True, no_sandbox=True, proxy="proxy1", uc_cdp=True,
        #                        uc_cdp_events=True)
        self.close_tab_by_domain(self.__driver, 'welcome.adblockplus.org')
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
            except:
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

    def fill_form(self):
        self.__driver.get(self.__config.get_config()['fafa_url'])
        self.__driver.find_element(By.CSS_SELECTOR, 'input#search1').send_keys(self.__config.get_config()['source_country'])
        self.__driver.find_element(By.CSS_SELECTOR, 'input#search10').send_keys(self.__config.get_config()['destination_country'])
        self.__driver.find_element(By.CSS_SELECTOR, 'div#typesb > table > tbody > tr:nth-of-type(3) > td > input').click()

    def main(self) -> False or True:
        self.fill_form()
        time.sleep(random.random() * 3)
        links_parts = self.__driver.current_url.split('?')
        for i in range(self.__config.get_config()['fafa_page_limit']):
            first_card = True
            self.__driver.get(f'{links_parts[0]}{i+1}/?{links_parts[1]}')
            time.sleep(5)
            cards = self.__driver.find_element(By.CSS_SELECTOR, 'html > body > table > tbody > tr:nth-of-type(2) > td > table:nth-of-type(2)').find_elements(By.XPATH, "//*[contains(@id,'res_')]")
            for card in cards:
                card_id = card.get_attribute('id')[4:]
                if self.__cards_parsed >= self.__config.get_config()['change_account_cards_limit'] and len(
                        self.__config.get_accounts_config_fafa()) > 1:
                    self.__cards_parsed = 0
                    if len(self.__config.get_accounts_config_fafa()) - 1 >= self.__creds_index:
                        self.__creds_index = 0
                    else:
                        self.__creds_index += 1
                    self.log_out()
                    time.sleep(5)
                    self.log_in(self.__config.get_accounts_config_fafa())
                    return False
                try:
                    button = card.find_element(By.CSS_SELECTOR, f'font#head_{card_id}')
                    self.__driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(2)
                    button.click()
                except:
                    self.__logger.info('button_dont_click')
                finally:
                    if first_card:
                        first_card = False
                        time.sleep(self.__config.get_config()['fafa_first_card_timeout'])
                    else:
                        time.sleep(self.__config.get_config()['timeout_cards_btn'])
                    try:
                        card.find_element(By.ID, random.choice(self.__buttons_ids)).click()
                        time.sleep(3)
                    except:
                        pass
                    self.parse_card(card_id, card)
                self.__cards_parsed += 1

    def __del__(self):
        self.__driver.quit()
