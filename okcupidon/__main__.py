#import configparser
#import argparse

def main():

    import time
    import random
    from .webship import WebDrive
    from .ourdatabase import dataBase

    okc_db = DataBase('okc_db')
    greeting = '''Welcome to the okcupid scraper interface.
The goal of this script is to recover profile info of okcupid.com users.'''
    print(greeting)

    my_scrapper = WebDrive()
    my_scrapper.log_to_ok_cupid()

    print('How many profiles would you like to scrape ? The data will be saved to a sqlite database called okc_db')
    # need to add type safety
    n = int(input('Amount of scraped profiles (please enter a number) : '))


    for _ in range(0,n):
        time.sleep(1)
        # Getting to the profile
        my_scrapper.get_to_full_profile()
        time.sleep(1)
        # Acquiring data
        decision = bool(random.randint(0, 1))
        okc_db.save_profile_to_db(dict_data=my_scrapper.acquire_data(),
                                  decision=decision)
        time.sleep(1)
        # Next profile
        my_scrapper.new_profile(decision=decision)
        time.sleep(1)

    okc_db.close()

if __name__ == '__main__':
    main()