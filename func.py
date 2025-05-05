from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import yaml
import string




class AccountMaker:
    def __init__(self, proxy=None):
        self.proxy = proxy # proxy string must be in format "IP:PORT"


    def run(self, cfg):
        # Creates chrome options and also the driver that will be used to control the browser.
        # If proxy present, use it. Else, no proxy is used.
        s = Service('/usr/bin/chromedriver')

        # Checks if a proxy is being used.
        if self.proxy: 
            options = Options()
            options.add_argument('--proxy-server=%s' % self.proxy)
            print(f"Using proxy: {self.proxy}")
            driver = webdriver.Chrome(options=options, service=s)
        else:
            driver = webdriver.Chrome(service=s)
        

        # visits page and waits
        driver.get('https://www.instagram.com/accounts/emailsignup/')
        time.sleep(5)


        #disable cookies
        try:
            cookies_prompt = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"))
            )
            cookies_prompt.click()
        except:
            print("Cookies prompt not found")


        #email input
        #email = cfg.randomize_email(input("Enter an email to send vercode to: "))
        email = input("Enter an email to send vercode to: ")
        email_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[4]/div/label/input')
        email_input.send_keys(email)


        #password input
        password_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[5]/div/label/input')
        password = cfg.get(item="password")
        password_input.send_keys(password)


        #full name input
        full_name_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[6]/div/label/input')
        
        firstname = cfg.get_random_fname()
        surname = cfg.get_random_sname()
        full_name = f"{firstname} {surname}"

        full_name_input.send_keys(full_name)

        #input()

        #username input
        username_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[7]/div/label/input')
        username = f"{firstname.lower()}.{surname.lower()}{''.join(random.choices(string.digits, k=6))}"
        username_input.send_keys(username)

        #next button
        next_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[8]/div/button')
        next_button.click()


        #birthday input
        #month
        month = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div/div[4]/div/div/span/span[1]/select/option[{random.randint(1,12)}]"))
        )
        month.click()

        #day
        day = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div/div[4]/div/div/span/span[2]/select/option[{random.randint(1,29)}]")
        day.click()

        #year
        year = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div/div[4]/div/div/span/span[3]/select/option[{random.randint(26, 66)}]")
        year.click()

        # another next button
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div/div[6]/button').click()


        #confirmation code
        confirmation_code = input("Enter confirmation code sent to inbox: ")
        conf_code_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div[2]/form/div/div[1]/input')
        conf_code_input.send_keys(confirmation_code)

        # third next button
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div[2]/form/div/div[2]').click()


        print(firstname,username,password,email)
        #temp
        input()
        driver.quit()


class Config:
    def __init__(self, path):
        self.path = path

    def get(self, item):
        with open(self.path) as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        try:
            item = cfg[item]
            return item
        except KeyError:
            print(f"{item} not in config")
            return None
        
    def randomize_email(self,email):
        s = email.split("@")
        s[0] += f"+{"".join(random.choices(string.ascii_letters, k=5))}"
        return "@".join(s)

    def get_random_proxy(self):
        with open("proxies.txt", "r") as f:
            proxy = random.choice(f.readlines())
        return proxy
    
    def get_random_fname(self):
        with open("firstnames.txt", "r") as f:
            contents = f.readlines()
        return random.choice(contents).replace("\n", "")
    
    def get_random_sname(self):
        with open("surnames.txt", "r") as f:
            contents = f.readlines()
        return random.choice(contents).replace("\n", "")