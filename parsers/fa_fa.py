#################################################
#                 created by                    #
#                     SBR                       #
#################################################
import json
import sys
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
            ['s_date2', By.CLASS_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME],
            ['tr', By.TAG_NAME]]
        self.__crud = CRUD(db)
        self.init()

    def parse_card(self, card_id, card_obj):
        output = [card_id]
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
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        4].text
                elif index == 5:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        3].text
                elif index == 6:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        5].find_elements(By.TAG_NAME, "div")[0].find_element(By.TAG_NAME, "a")
                elif index == 7:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        5].find_element(By.TAG_NAME, "td").find_elements(By.TAG_NAME, "div")[1].text
                elif index == 8:
                    data = card_obj.find_elements(element[1], element[0])[0].find_elements(By.TAG_NAME, "td")[
                        3].text
            except:
                match index:
                    case 0:
                        self.error_parse(output, 2)
                    case 1:
                        self.error_parse(output, 1)
                    case 2:
                        self.error_parse(output, 2)
                    case 3:
                        self.error_parse(output, 4)
                    case 4:
                        self.error_parse(output, 2)
                    case 5:
                        self.error_parse(output, 1)
                    case 6:
                        self.error_parse(output, 2)
                    case 7:
                        self.error_parse(output, 4)
                    case 8:
                        self.error_parse(output, 2)
                    case _:
                        self.error_parse(output)
                continue
            # Дата добавления и изменения
            if index == 0:
                monthes = {'января': "01", 'февраля': "02", 'марта': "03", 'апреля': "04", 'мая': "05", 'июня': "06",
                           'июля': "07", 'августа': "08", 'сентября': "09", 'октября': "10", 'ноября': "11", 'декабря': "12",}
                try:
                    data = data.split('\n')
                    if '-' in data[0]:
                        data[0] = data[0][6:]
                    output.extend([None, None])
                    for i in range(2):
                        try:
                            if data[i+2][:4] == "изм.":
                                if ':' in data[i+2][6:]:
                                    formated_date = f'{data[0]}.{datetime.now().year} {data[i+2][6:]}'
                                else:
                                    formated_date = f'{data[i+2][6:8]}.{monthes[data[i+2][9:]]}.{datetime.now().year} 00:00'
                                date_time_obj = datetime.strptime(formated_date, "%d.%m.%Y %H:%M")
                                output[-1] = date_time_obj
                            elif data[i+2][:4] == "доб.":
                                if ':' in data[i+2][6:]:
                                    formated_date = f'{data[0]}.{datetime.now().year} {data[i+2][6:]}'
                                else:
                                    formated_date = f'{data[i+2][6:8]}.{monthes[data[i+2][9:]]}.{datetime.now().year} 00:00'
                                date_time_obj = datetime.strptime(formated_date, "%d.%m.%Y %H:%M")
                                output[-2] = date_time_obj
                            print(output)
                        except:
                            pass
                except:
                    pass
            elif index == 1:
                output.append(data)
                print(output, 'transport_type')
            elif index == 2:
                try:
                    data = data.split('/')
                    weight = data[0][:-2]
                    volume = data[1][1:-2]
                    if ',' in weight:
                        weight = weight.replace(',', '.')
                    elif ',' in volume:
                        volume = volume.replace(',', '.')
                    output.extend([float(weight), float(volume)])
                    print(output, 'weight and volume')
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
                    print(output, 'cities')
                except Exception as e:
                    print(e)
                    self.error_parse(output, 4)
            elif index == 4:
                try:
                    data = data.split('\n')[1]
                    output.extend([data, None])
                except:
                    self.error_parse(output, 2)
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
                    output.extend([data.text, data.get_attribute('href')])
                    print(output, 'company')
                except:
                    self.error_parse(output, 2)
            elif index == 7:
                temp = [None, None, None, None]
                try:
                    data = data.replace('\n', ' ')
                    print(data, 'phones')
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
                    print(output, 'creds')
                except:
                    self.error_parse(output, 4)
            elif index == 8:
                success = False
                try:
                    data = data.split('\n')[2:]
                    print(data, 'prices')
                    for i in data:
                        if ' тнг' in i:
                            success = True
                            price = i[:i.index(' тнг')]
                            if '.' in price:
                                price = price.replace('.', '')
                                output.extend([price, None])
                                print(output, 'price')
                                break
                    if not success:
                        raise
                except Exception as e:
                    print(e)
                    self.error_parse(output, 2)
        self.__logger.info(output)
        try:
            output.append('НОВАЯ')
            print(output, 'itog')
            self.__crud.add_application(output)
        except:
            pass

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
        # , headless2=True, headed=False, agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        self.__driver = Driver(uc=True, no_sandbox=True, proxy="proxy1", uc_cdp=True,
                               uc_cdp_events=True, extension_dir='./adblock')
        time.sleep(20)
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

    def fill_form(self):
        self.__driver.get(self.__config.get_config()['fafa_url'])
        self.__driver.find_element(By.CSS_SELECTOR, 'input#search1').send_keys('Казахстан')
        self.__driver.find_element(By.CSS_SELECTOR, 'input#search10').send_keys('Казахстан')
        self.__driver.find_element(By.CSS_SELECTOR, 'div#typesb > table > tbody > tr:nth-of-type(3) > td > input').click()


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
                    # self.close_sign_up_menu()
                    # time.sleep(random.random() * 3)
                    self.log_out()
                    time.sleep(5)
                    self.log_in(self.__config.get_accounts_config_fafa())
                    return False
                if self.__crud.check_already_existed(int(card_id)):
                    if self.recheck_card(card_id, card):
                        continue
                    else:
                        return True
                else:
                    try:
                        button = card.find_element(By.CSS_SELECTOR, f'font#head_{card_id}')
                        self.__driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(1)
                        button.click()
                    except:
                        self.__logger.info('button_dont_click')
                    finally:
                        if first_card:
                            first_card = False
                            time.sleep(self.__config.get_config()['fafa_first_card_timeout'])
                        else:
                            time.sleep(self.__config.get_config()['timeout_cards_btn'])
                        #.find_elements(By.TAG_NAME, 'td')[random.randint(0, 3)].find_element(By.TAG_NAME, 'input').click()
                        #print(card.find_elements(By.TAG_NAME, 'tr')[2].find_element(By.TAG_NAME, 'tr').find_element(By.TAG_NAME, 'tr').text)
                        self.parse_card(card_id, card)
                self.__cards_parsed += 1

    def __del__(self):
        self.__driver.quit()
