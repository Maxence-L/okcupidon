import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selexcept
# import requests
import re
import pickle
import random
import json
from .dataparser import parse_profile

class WebDrive:

    # Initialize the webdriver, loading target url and the cookies
    def __init__(self, cookies=None):

        def __start_webdriver():
            options = Options()
            options.add_argument('window-size=1200x1000')
            return webdriver.Chrome(chrome_options=options)

        def __load_cookies():
            # Let's try to load user-provided cookies
            if os.path.isfile('cookies.json'):
                try :
                    with open('cookies.json', 'r') as ck :
                        mein_cookies = json.load(ck)
                    print('cookies.json was found')
                    return mein_cookies
                except FileNotFoundError:
                    pass

            # Let's see if we saved previous cookies before
            if os.path.isfile('cookies.pkl'):
                try:
                    mein_cookies = pickle.load(open("cookies.pkl", "rb"))
                    print('Cookies saved by pickle during preceding sessions were found')
                    return mein_cookies
                except EOFError:
                    pass

        self.driver = __start_webdriver()
        self.cookies = __load_cookies()
        self.website = 'https://www.okcupid.com'

    def log_to_ok_cupid(self):
        """This method is used to log to OK_Cupid.
        It searches first for cookies that may have been created before.
        If there are no cookies, it will pass the 2FA using __two_FA()
        and then save the cookies for a quicker log-in later."""

        def __two_fa(self, email=None, pwd=None):
            """This function is used in case where no cookies are provided or OKCupid asks nonetheless
            for a password and a 2FA"""
            """Log to OKCupid with the id provided"""
            print("We'll log in manually to OKCupid, as no valid cookies were found")
            if email == None or pwd == None:
                email = input("Please enter your profile email: ")
                pwd = input("Please enter your password: ")

            # login window access
            self.driver.get(self.website + "/login")
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.ID, "username")))
            finally:
                pass
            # Passing the auth info
            self.driver.find_element_by_name("username").send_keys(email)
            self.driver.find_element_by_id('password').send_keys(pwd)

            # Proceed with the login
            self.driver.find_element_by_class_name("login-actions-button").click()
            time.sleep(5)

            # If OKCupid asks for 2FA :
            if self.driver.current_url != 'https://www.okcupid.com/home':
                try:
                    self.driver.find_element_by_class_name("login-actions-button").click()
                    time.sleep(5)

                    # Logging the sms code - prepare to get your SMS
                    code = input('Please enter the six digits (ex : 123456) received by SMS :')
                    code_digits = self.driver.find_elements_by_css_selector("input.code-inputs-digit")

                    for digit in range(6):
                        code_digits[digit].send_keys(code[digit])
                        time.sleep(3)
                except selexcept.NoSuchElementException:
                    pass
                # Clicking on the "next" button
                self.driver.find_element_by_class_name("login-actions-button").click()

            if self.driver.current_url == 'https://www.okcupid.com/home':
                pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
                print("Cookies were saved")

        # login window access
        self.driver.get(self.website + "/login")
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "username")))
        finally:
            pass

        # Loading cookies if present.
        if self.cookies is not None:
            self.driver.get(self.website)
            for cookie in self.cookies:
                self.driver.add_cookie(cookie)
            print("Cookies were loaded")

        # Close the cookies warning in case it is still here
        try:
            self.driver.find_element_by_id('onetrust-accept-btn-handler').click()
        except selexcept.NoSuchElementException:
            pass

        # Try to get to the home interface
        self.driver.get(self.website+'/home')
        time.sleep(5)

        # If this doesn't work (typically, cookies aren't that fresh), we log-in manually
        cant_connect = self.cookies is None or self.driver.current_url != 'https://www.okcupid.com/home'
        print(self.driver.current_url)
        if cant_connect is True:
            __two_fa(self)
        time.sleep(5)

    def get_current_url(self):
        return self.driver.current_url

    def get_to_full_profile(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'cardsummary')))
            self.driver.find_element_by_link_text('View Profile').click()
        except (selexcept.TimeoutException, selexcept.NoSuchElementException):
            self.driver.get(self.website+'/doubletake')
            
    def acquire_data(self):
        """The main profile scraper :
        acquires all of the personnal data that is on the profile page
        and returns it as a dict"""

        # Open the full essays
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main_content"]/div[3]/div[1]/div[1]/div/button/span')))
            self.driver.find_element_by_xpath('//*[@id="main_content"]/div[3]/div[1]/div[1]/div/button/span').click()
        except (selexcept.NoSuchElementException, selexcept.TimeoutException):
            pass

        # Uncomment if you want to save to last profile's .html file (for debugging reasons)
        # with open('profile.html', 'w') as file:
            # file.write(self.driver.page_source)
            # file.close()

        # Parse the profile
        profile_id = re.search('(?<=\/)(\d*?)(?=\?)', self.driver.current_url).group(0)
        data = parse_profile(profile_id=profile_id, html_page=self.driver.page_source)

        return data

    def new_profile(self, decision):
        """Brings the driver to a new profile"""
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, "like-button")))
        if decision:
            self.driver.\
                find_element_by_xpath('/html/body/div[1]/main/div[1]/div[2]/div/div/div[3]/span/div/button[2]').\
                click()
            self.driver.get('https://www.okcupid.com/doubletake')
        else :
            self.driver.\
            find_element_by_xpath("/html/body/div[1]/main/div[1]/div[2]/div/div/div[3]/span/div/button[1]").\
            click()
