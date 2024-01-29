from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas, time, pickle

class Cookies:
    def __init__(self):
        #load in accounts and such
        self.accounts = pandas.read_csv('accounts.csv')
        return
    
    def testCookies(self):
        #test cookies
        return
    
    def updateCookies(self):
        #for each account
        n = self.accounts.shape[0]
        print(n)
        for i in range(n):
            #bot automates login
            web = webdriver.Chrome()
            web.get('https://www.tiktok.com/login/phone-or-email/email')
            element = WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginContainer"]/div[1]/form/div[1]/input')))
            element.send_keys(self.accounts['username'][i])
            element = WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginContainer"]/div[1]/form/div[2]/div/input')))
            element.send_keys(self.accounts['password'][i])
            element = WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginContainer"]/div[1]/form/button')))
            element.click()
            #user completed capcha
            element = WebDriverWait(web, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-header"]/div/div[3]/div[1]/a')))
            #bot saves cookies
            time.sleep(5)
            pickle.dump(web.get_cookies(), open(f"cookies/{self.accounts['username'][i]}.pkl", "wb"))
        return

if __name__ == "__main__":
    cookies = Cookies()
    cookies.updateCookies()