import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selexcept
import re
import pickle
import json
from .dataparser import parse_profile
import sys
from webdriver_manager.chrome import ChromeDriverManager


class WebDrive:

    def __init__(self, cookies=None):

        """Initialize the webdriver, loading target url and the cookies. """

        def __start_webdriver():

            try:
                options = Options()
                options.add_argument('window-size=1200x1000')
                return webdriver.Chrome(chrome_options=options)

            except selexcept.SessionNotCreatedException:
                from webdriver_manager.chrome import ChromeDriverManager
                options = Options()
                options.add_argument('window-size=1200x1000')
                return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

        def __load_cookies():
            # Let's try to load user-provided cookies
            cookies_found = False
            if cookies is not None and os.path.isfile(cookies):
                try :
                    with open(cookies, 'r') as ck :
                        mein_cookies = json.load(ck)
                        ck.close()
                    print('cookies.json was found')
                    cookies_found = True
                    return mein_cookies

                except FileNotFoundError:
                    print(f"We couldn't find the cookies at {cookies}")
                    pass

            # Let's see if we saved previous cookies before
            if os.path.isfile('cookies.pkl'):
                try:
                    mein_cookies = pickle.load(open("cookies.pkl", "rb"))
                    print('Cookies saved by pickle during preceding sessions were found')
                    cookies_found = True
                    return mein_cookies
                except EOFError:
                    print("We can't load the cookies saved during preceding sessions")
                    pass

            # If no usable cookies were found, we return a None value
            if cookies_found == False:
                return None

        self.driver = __start_webdriver()
        self.user_cookies = __load_cookies()
        self.website = 'https://www.okcupid.com'

    # End of __init__


    def log_to_ok_cupid(self, id=None, pwd=None, save_cookies=True):

        """This method is used to log to OK_Cupid.

        It searches first for cookies that may have been created before.
        If there are no cookies, it will pass the 2FA using __two_FA()
        and then save the cookies for a quicker log-in later. """

        ##### Utils functions #####

        def __two_fa_login(id, pwd, save_cookies=True):

            """This function is used in case where no cookies are provided or OKCupid asks nonetheless
            for a password and a 2FA"""

            print("You provided and email and a password which will be used for logging in")
            # login window access
            self.driver.get(self.website + "/login")
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.ID, "username")))
            finally:
                pass
            # Passing the auth info
            self.driver.find_element_by_name("username").send_keys(id)
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
                time.sleep(5)
            saving_cookies = self.driver.current_url == 'https://www.okcupid.com/home' and save_cookies
            print(self.driver.current_url == 'https://www.okcupid.com/home')
            print(saving_cookies)
            print(save_cookies)
            print(self.driver.current_url)

            if saving_cookies:
                pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
                print("Cookies were saved")

        def __cookies_login(self):

            # Loading cookies if present.
            if self.user_cookies is not None:
                self.driver.get(self.website)
                for cookie in self.user_cookies:
                    self.driver.add_cookie(cookie)
                print("Cookies were loaded")

            # Close the cookies warning in case it is still here
            try:
                self.driver.find_element_by_id('onetrust-accept-btn-handler').click()
            except selexcept.NoSuchElementException:
                pass

            # Try to get to the home interface
            self.driver.get('https://www.okcupid.com/home')
            time.sleep(5)

            # If this doesn't work (typically, cookies aren't that fresh), we log-in manually
            cant_connect = (self.user_cookies is None) or \
                           (self.driver.current_url != 'https://www.okcupid.com/home')
            if cant_connect:
                print("No usuable cookies were found. Please try entering your id info (id, pwd)")

                return cant_connect

        ###### Function starts here #######

        if __cookies_login(self) and ((pwd != 'None') and (id != 'None')) :
           __two_fa_login(id=id, pwd=pwd, save_cookies=save_cookies)

    def get_current_url(self):
        return self.driver.current_url

    def get_to_full_profile(self, wait_time=4):
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'cardsummary')))
            time.sleep(wait_time)
            self.driver.find_element_by_link_text('View Profile').click()
        except (selexcept.TimeoutException, selexcept.NoSuchElementException):
            self.driver.get(self.website+'/doubletake')

    def acquire_data(self, wait_time=4):
        """The main profile scraper

        Acquires all of the personal data that is on the profile page
        and returns it as a dict"""

        # Open the full essays
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main_content"]/div[3]/div[1]/div[1]/div/button/span')))
            time.sleep(wait_time)
            self.driver.find_element_by_xpath('//*[@id="main_content"]/div[3]/div[1]/div[1]/div/button/span').click()
        except (selexcept.NoSuchElementException, selexcept.TimeoutException):
            pass

        # Parse the profile
        try :
            profile_id = self.driver.current_url[32:51]
        except IndexError :
            print(self.driver.current_url)
            time.sleep(wait_time+4)
            profile_id = self.driver.current_url[32:51]

        if profile_id is None :
            print(self.driver.current_url)
        data = parse_profile(profile_id=profile_id, html_page=self.driver.page_source)
        time.sleep(wait_time)

        return data

    def new_profile(self, decision):
        """Brings the driver to a new profile """
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, "like-button")))
        time.sleep(2)
        if decision:
            self.driver.\
                find_element_by_xpath('/html/body/div[1]/main/div[1]/div[2]/div/div/div[3]/span/div/button[2]').\
                click()
            self.driver.get('https://www.okcupid.com/doubletake')
        else:
            self.driver.\
            find_element_by_xpath("/html/body/div[1]/main/div[1]/div[2]/div/div/div[3]/span/div/button[1]").\
            click()

    def debug(self):
        self.take_screenshot()
        print(self.driver.current_url)
        with open('profile.html', 'w') as file:
            file.write(self.driver.page_source)
            file.close()

    def take_screenshot(self):
        """Takes a screenshot of the driver's current state"""
        self.driver.get_screenshot_as_file('driver_screenshot.png')