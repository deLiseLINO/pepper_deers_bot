from selenium import webdriver
from data import login_list, password
from time import time, ctime, sleep
from datetime import datetime
from multiprocessing import Pool
from random import randint
import logging

from selenium.common.exceptions import NoSuchElementException


logging.basicConfig(level=logging.WARNING, format='%(asctime)s:%(levelname)s:%(message)s')


class Pepper:
    def __init__(self, login, headless=True):
        options = webdriver.ChromeOptions()
        options.headless = headless
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome('chromedriver.exe', options=options)
        self.login = login
        self.sleep = sleep
        self.working = self.sign_in(self.login)
        s = 1

    def sign_in(self, login):
        """Authorization"""
        rndint = randint(5, 260)
        sleep(rndint)
        self.driver.get("https://www.pepper.ru/")
        #sleep(randint(0, 100)/10)
        #self.driver.find_element_by_class_name("btn--mode-header").click()
        self.driver.find_element_by_xpath("/html/body/main/div[1]/header/div/div/div[3]/button[2]").click()
        sleep(1)
        self.driver.find_element_by_id("loginModalForm-identity").send_keys(login)
        self.driver.find_element_by_id("loginModalForm-password").send_keys(password)
        sleep(1)


        self.driver.find_element_by_class_name("cept-login-submit").click()
        sleep(3)
        if self.xpath_exists("//button[contains(@class, 'btn--mode-header')]"):
            print(ctime(time()), login, "FAILED TO LOG IN")
            self.close_driver()
            return False
        else:
            print(ctime(time()), login, "logged in")
            return True

    def xpath_exists(self, xpath):
        """ Checks element by xpath"""
        try:
            self.driver.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    def catch(self):
        """Catches deers"""

        while True:
            sections = [
                "new",
                "discussed",
                "hot"
            ]
            try:
                self.driver.find_element_by_class_name("supportImage--type-embarrassed")
                logging.warning(f"BANNED {self.login}")
                print(f"{self.login} BANNED")
            except: pass
            self.driver.get(f"https://www.pepper.ru/{sections[randint(0, 2)]}")
            #self.driver.get("https://www.pepper.ru/flamedeer/collection")
            logging.info(f" reloaded {self.login}")
            sleep(1)
            rndint = randint(0, 10)
            self.driver.find_elements_by_class_name("thread-title--list")[rndint].click()
            
            minutes_to_update = 1
            #for seconds in range(60*minutes_to_update):
            for seconds in range(randint(20, 100)):
                try:
                    self.driver.find_element_by_class_name("mc-btn--primary").click()
                    print(ctime(time()), self.login, seconds)
                    dtime = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
                    sleep(0.5)
                    self.driver.get_screenshot_as_file(f"media\{dtime} {self.login}.png")
                    #break
                #except NoSuchElementException:
                except:
                    sleep(1)


    def parse_deers_quantity(self):
        """Parses deers quantity"""
        self.driver.find_element_by_class_name("js-avatar").click()
        sleep(1)
        name = self.driver.find_element_by_class_name("navDropDown-head").text

        self.driver.get("https://www.pepper.ru/flamedeer/collection")
        grid_elements = self.driver.find_elements_by_class_name("space--fromW3-r-3")
        del grid_elements[-1]
        grid_elements = [elem.text for elem in grid_elements] 
        deers_quantity = []
        set_quantity = []
        for elem in grid_elements:
            quantity = [int(s) for s in elem.split() if s.isdigit()]
            if len(quantity) != 0:
                set_quantity.append(int(quantity[0]))
            else:
                set_quantity.append(0)
            if len(set_quantity) == 3 and len(deers_quantity) < 6:
                deers_quantity.append(set_quantity)
                set_quantity = []
        self.driver.quit()
        #return([deers_quantity, name])
        return([deers_quantity, self.login])
    
    def send_trade(self, name, where_to_get_path, extra_path):
        """Send trade offer"""
        from data import names
        self.driver.get("https://www.pepper.ru/flamedeer/trade")
        sleep(2)
        self.driver.find_element_by_class_name("cept-trading-partner-user-search-suggestions").send_keys(name)
        sleep(2.5)
        self.driver.find_element_by_class_name("autoSuggest-suggestion").click()
        self.driver.find_element_by_class_name("js-step1Submit").click()
        sleep(1)


        deers = self.driver.find_elements_by_class_name("ratioBox-child")
        for deer in deers:
            if deer.get_attribute("alt") == f"{names[where_to_get_path[1]]}-{where_to_get_path[2] + 1}":
                deer.click()
                break
        sleep(1)
        self.driver.find_element_by_class_name("cept-next-button").click()

        sleep(1)
        deers = self.driver.find_elements_by_class_name("ratioBox-child")
        for deer in deers:
            #if deer.get_attribute("alt") == "dove-1":
            if deer.get_attribute("alt") == f"{names[extra_path[1]]}-{extra_path[2] + 1}":
                deer.click()
                break
        sleep(1)
        self.driver.find_element_by_class_name("cept-next-button").click()

        self.driver.find_element_by_class_name("js-step3Submit").click()
        #sleep(30)

            #print(deer.get_attribute("alt"))
        #[deer.click() for deer in deers if deer.get_attribute("alt") == "dove-1"]
        #self.driver.find_element_by_xpath("//img[contains(@alt, 'dove-1')]").click()
        pass

    def accept_last_trade(self):
        self.driver.get("https://www.pepper.ru/flamedeer/trade-requests")
        self.driver.find_element_by_class_name("cept-accept").click()
        self.close_driver()

def catch_deers(login):
    p = Pepper(login)
    p.catch()

def parse(login):
    p = Pepper(login)
    if p.working == True:
        return p.parse_deers_quantity()
    else: return

def trade_deers():
    amount = len(login_list)
    login_list.reverse()
    print(amount, "accounts trading")
    p = Pool(processes=amount)
    result = p.map(parse, login_list)
    [r[0].reverse() for r in result]
    [print(s) for s in result]
    for j in range(len(result)):
        quantity = result[j][0]
        need_to_get_paths = []
        where_to_get_paths = []
        extra_paths = []
        for i in range(len(quantity)):
            arr = [1, 0]
            for p in arr:
                if quantity[i][p] == 0:
                    for z in range(len(result)):
                        if z == j: continue
                        if result[z][0][i][p] > 1:
                            need_to_get_paths.append([j, i, p])
                            where_to_get_paths.append([z, i, p])
                            break
                elif quantity[i][p] > 1:
                    extra_paths.append([j, i, p])

            if quantity[i][1] == 0 and quantity[i][0] > 0:
                for z in range(len(result)):
                    if z == j: continue
                    if result[z][0][i][1] > 0 and result[z][0][i][0] == 0:
                        need_to_get_paths.append([j, i, 1])
                        where_to_get_paths.append([z, i, 1])
                        break


                            
        if len(where_to_get_paths) != 0 and len(extra_paths) != 0:
            p = Pepper(login_list[extra_paths[0][0]], headless=False)
            for i in range(len(extra_paths)):
                if len(where_to_get_paths) > i:
                    name = result[where_to_get_paths[i][0]][1]
                    p.send_trade(name, where_to_get_paths[i], extra_paths[i])
                    result[extra_paths[i][0]][0][extra_paths[i][1]][extra_paths[i][2]] -= 1
                    result[where_to_get_paths[i][0]][0][extra_paths[i][1]][extra_paths[i][2]] += 1

                    result[where_to_get_paths[i][0]][0][where_to_get_paths[i][1]][where_to_get_paths[i][2]] -= 1
                    result[extra_paths[i][0]][0][where_to_get_paths[i][1]][where_to_get_paths[i][2]] += 1

                    [print(s) for s in result]
                    print()
                    p2 = Pepper(login=login_list[where_to_get_paths[i][0]], headless=True)
                    p2.accept_last_trade()
            p.close_driver()


    for acc in result:
        sets = 0
        for set_ in acc[0]:
            if int(set_[0]) > 0 and int(set_[1]) > 0:
                sets += 1
        print(str(sets) + " sets")
            



if __name__ == "__main__":
    # login_list = [login_list[0]]



    amount = len(login_list)
    print(amount, "accounts")
    p = Pool(processes=amount)
    p.map(catch_deers, login_list)

    #catch_deers(login_list[1])

    #trade_deers()




            
        
