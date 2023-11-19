# config.py


import configparser

read_config = configparser.ConfigParser()
read_config.read('settings.ini')


bot_token = read_config['settings']['token'].strip()
PATH_DATABASE = 'data/database.db'

for section in read_config.sections():
    print(f"Section: {section}")
    for key, value in read_config.items(section):
        print(f"  {key} = {value}")








# Initialize the dispatcher


# Получение администраторов бота
def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read('settings.ini')

    admins = read_admins['settings']['admin_id'].strip()
    admins = admins.replace(' ', '')

    if ',' in admins:
        admins = admins.split(',')
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while '' in admins: admins.remove('')
    while ' ' in admins: admins.remove(' ')
    while '\r' in admins: admins.remove('\r')

    admins = list(map(int, admins))

    return admins





