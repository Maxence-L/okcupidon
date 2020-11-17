import configparser
import argparse
import time
import random
from .webship import WebDrive
from .ourdatabase import DataBase
import os
import traceback

def main():

    # Parse config.ini
    config = configparser.ConfigParser(allow_no_value=True)

    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'config.ini')
    config.read(config_filename)

    # We add parsable arguments for ease of use
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subroutine')

    # Identification args
    parser.add_argument('-i', '--id',
                        default=config['global']['id'],
                        help = 'The email used to log in Okcupid \n')
    parser.add_argument('-p', '--pwd',
                        default=config['global']['pwd'],
                        help = 'The password used to log in Okcupid \n')
    parser.add_argument('-c', '--cookies_file',
                        default=config['global']['cookies_file'],
                        help = 'Name or absolute path to the .json file'
                               'containing the OKC cookies (credentials)'
                               'necessary to view user profiles. \n')
    parser.add_argument('-s', '--store_cookies',
                        action='store_true',
                        default=config['global']['store_cookies'],
                        help = 'Store session cookies as a .pkl file '
                               '- useful if you are logging for the first time'
                               'using id and pwd \n')

    # Args about config file
    parser.add_argument("--no-save-config",
                        action='store_false',
                        default=True,
                        dest='save_config',
                        help='If used, any other cl-args provided are not '
                             'saved to the config.ini file. This arg does '
                             'not require a value. \n')
    parser.add_argument('--print-config',
                      action="store_true",
                      help='Print contents of config file. \n')

    # Utils args
    parser.add_argument('--max-query-attempts',
                        type=int,
                        default=config['global']['max_query_attempts'],
                        help='The number of attempts to make when requesting '
                             'a webpage, in case the first request is not '
                             'successful. \n')

    parser.add_argument('--outfile',
                             default=config['global']['outfile'],
                             dest='outfile',
                             help='Name or absolute path of the sql file in which '
                                  'to store the collected usernames. \n')

    parser.add_argument('--num-profiles',
                            default=config['global']['num_profiles'],
                            help='Integer specifying the number of profiles to browse.' 
                            'Set by default to 3, for testing purposes \n',
                            dest='num_profiles',
                            type=int)

    # Actions
    parser_print = subparsers.add_parser('print_config',
                                        help = 'Print contents of config file. \n')

    parser_run = subparsers.add_parser('run',
                                       help = 'Run the webscrapper. \n')
    
    parser_run.add_argument('-d, --debug_mode',
                            action='store_true',
                            default=False,
                            dest='debug_mode',
                            help='Activates debug mode in case the scrapper encounters problems :'
                                 '- Takes a screenshot of the problematic webpage'
                                 '- Saves the html of the problematic webpage'
                                 '- Prints the error'
                                 'All files are saved in the current directory \n')

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

    #######
    # routines :
    #######

    # Print config
    if args_obj['subroutine'] == 'print_config' :
        print_config(config)

    # Run the scrapper
    elif args_obj['subroutine'] == 'run':

        # We set up the database
        okc_db = DataBase(outfile)

        # We start the scrapper
        my_scrapper = WebDrive(cookies=cookies_file)

        # Logging to Okcupid
        my_scrapper.log_to_ok_cupid(id=id, pwd=pwd, save_cookies=store_cookies)

        # Looping through all of the profiles

        activity = 0
        for i in range(0,num_profiles):
            time.sleep(1)

            # Setting a fuse in case of unsuccessful query
            fuse = 0
            for i in range(0, max_query_attempts):
                # Getting to the profile
                try:
                    my_scrapper.get_to_full_profile()
                    time.sleep(5)
                    # Acquiring data
                    decision = bool(random.randint(0, 1))

                    data = my_scrapper.acquire_data()

                    okc_db.save_profile_to_db(dict_data=data,
                                              decision=decision)
                    time.sleep(1)
                    # Next profile
                    my_scrapper.new_profile(decision=decision)
                    time.sleep(1)
                    break
                except :
                    traceback.print_exc(limit=1, chain=True)
                    fuse +=1
                    pass

            activity += 1
            if fuse == max_query_attempts:

                if args_obj['debug_mode'] :
                    my_scrapper.debug()
                    traceback.print_exc(limit=1, chain=True)

                print(f"Max query attempts reached on {my_scrapper.get_current_url} - stopping the scrapper.")
                break
        print(f"{activity} profiles were parsed")

        okc_db.close()

# Save config
def __save_config(config, args_obj) :
    """Save the current configs in the .ini file.
    """

    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'config.ini')
    for key in config['global'].keys():
        if key in args_obj.keys():
            config.set('global', key, str(args_obj[key]))

    with open(config_filename, 'w') as f:
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