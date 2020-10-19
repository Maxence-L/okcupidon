import configparser
import argparse
import time
import random
from webship import WebDrive
from ourdatabase import DataBase
import os

def main():

    # Parse config.ini
    config = configparser.ConfigParser(allow_no_value=True)

    pkg_root_path = os.path.dirname(__file__)
    config_path = os.path.join(pkg_root_path, 'config.ini')
    print(config_path)
    config.read(config_path)

    # We add parsable arguments for ease of use
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subroutine')

    # Identification args
    parser.add_argument('-i', '--id',
                        default=config['global']['id'],
                        help = 'The email used to log in Okcupid')
    parser.add_argument('-p', '--pwd',
                        default=config['global']['pwd'],
                        help = 'The password used to log in Okcupid')
    parser.add_argument('-c', '--cookies_file',
                        default=config['global']['cookies_file'],
                        help = 'Name or absolute path to the .json file'
                               'containing the OKC cookies (credentials)'
                               'necessary to view user profiles.')
    parser.add_argument('-s', '--store_cookies',
                        action='store_true',
                        help = 'Store session cookies as a .pkl file '
                               '- useful if you are logging for the first time'
                               'using id and pwd')

    # Args about config file
    parser.add_argument("--no-save-config",
                        action='store_false',
                        default=True,
                        dest='save_config',
                        help='If used, any other cl-args provided are not '
                             'saved to the config.ini file. This arg does '
                             'not require a value.')
    parser.add_argument('--print-config',
                      action="store_true",
                      help='Print contents of config file.')

    # Utils args
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

    # Actions
    parser_print = subparsers.add_parser('print_config',
                                        help = 'Print contents of config file.')

    parser_run = subparsers.add_parser('run',
                                       help = 'Run the webscrapper.')

    parser_run = subparsers.add_parser('--num-profiles',
                              type=int,
                              default=config['global']['num_profiles'],
                              help='Integer specifying the number of profiles '
                                   'to browse.')

    # vars() because we need to be able to access the contents like obj[str]
    args_obj = vars(parser.parse_args())

    # We can now define global parameters
    cookies_file = args_obj['cookies_file']
    save_config = args_obj['save_config']
    store_cookies = args_obj['store_cookies']
    pwd = args_obj['pwd']
    id = args_obj['id']
    outfile = args_obj['outfile']
    max_query_attempts = args_obj['max_query_attempts']
    num_profiles = args_obj['num_profiles']

    if save_config :
        __save_config(config, args_obj)

    if args_obj['subroutine'] == 'print_config' :
        print_config(config)

    elif args_obj['subroutine'] == 'run':

        #We set up the database
        okc_db = DataBase(outfile)

        # We start the scrapper
        my_scrapper = WebDrive(cookies=cookies_file)
        my_scrapper.log_to_ok_cupid(id=id, pwd=pwd, save_cookies=store_cookies)

        for i in range(0,args_obj['num_profiles']):
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

# Save config
def __save_config(config, args_obj) :
    """Save the current configs in the .ini file.
    """
    for key in config['global'].keys():
        if key in args_obj.keys():
            config.set('global', key, str(args_obj[key]))

    with open('config.ini', 'w') as f:
        config.write(f)

def print_config(config) :
    """Print all parameters in the config.ini file in a readable format.
    """
    for section in config.sections():
        print('[{}]'.format(section))
        for key in config[section]:
            print('{} = {}'.format(key, config[section][key]))
        print('')

if __name__ == '__main__':
    main()