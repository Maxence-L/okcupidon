import configparser
import argparse
import time
import random
from webship import WebDrive
from ourdatabase import DataBase
import os

def main():

    # Parse config.ini
    config = configparser.ConfigParser()

    pkg_root_path = os.path.dirname(__file__)
    config_path = os.path.join(pkg_root_path, 'config.ini')
    print(config_path)
    config.read(config_path)

    parser = argparse.ArgumentParser()

    parser.add_argument('--num-profiles',
                              type=int,
                              default=config['global']['num_profiles'],
                              help='Integer specifying the number of profiles '
                                   'to browse.')

    # Identification args
    parser.add_argument('-i', '--id',
                        default=config['global']['id'],
                        help = 'The email used to log in Okcupid')
    parser.add_argument('-p', '--pwd',
                        default=config['global']['pwd'],
                        help = 'The password used to log in Okcupid')
    parser.add_argument('-c', '--cookies_file',
                        help = 'Name or absolute path to the .json file'
                               'containing the OKC cookies (credentials)'
                               'necessary to view user profiles.')
    parser.add_argument('-s', '--store_cookies',
                        action='store_true',
                        help = 'Store session cookies as a .pkl file '
                               '- useful if you are logging for the first time'
                               'using id and pwd')

    # Save config
    parser.add_argument('--no-save-config',
                        action='store_false',
                        default=True,
                        dest='save_config',
                        help='If used, any other cl-args provided are not '
                             'saved to the config.ini file. This arg does '
                             'not require a value.')
    parser.add_argument('-p', '--print-config',
                      action="store_true",
                      help='Print contents of config file.')

    # Utils args
    parser.add_argument('--webdriver_path',
                        help='Specify the path of the webdriver. Can be '
                             'relative to the package root path or absolute.')
    parser.add_argument('--max-query-attempts',
                        type=int,
                        default=config['global']['max_query_attempts'],
                        help='The number of attempts to make when requesting '
                             'a webpage, in case the first request is not '
                             'successful.')
    parser.add_argument('--outfile',
                             default=config['global']['outfile'],
                             dest='usernames_outfile',
                             help='Name or absolute path of the sql file in which '
                                  'to store the collected usernames.')

    args = parser.parse_args()

    okc_db = DataBase('okc_db')

    my_scrapper = WebDrive(cookies=args.cookies_file)
    my_scrapper.log_to_ok_cupid(id=args.id, pwd=args.pwd, save_cookies=args.store_cookies)

    for i in range(0,10):
        time.sleep(1)
        # Getting to the profile
        try:
            my_scrapper.get_to_full_profile()
            time.sleep(5)
            # Acquiring data
            decision = bool(random.randint(0, 1))
            okc_db.save_profile_to_db(dict_data=my_scrapper.acquire_data(),
                                      decision=decision)
            time.sleep(1)
            # Next profile
            my_scrapper.new_profile(decision=decision)
            time.sleep(1)
        except :
            pass
        print(i)

    okc_db.close()

if __name__ == '__main__':
    main()