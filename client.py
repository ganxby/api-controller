from controller import ManagerAPI

import sys
import json
import asyncio


f = open('config.json', 'r')
parsed_file = json.load(f)

api = ManagerAPI(login=parsed_file['login'], password=parsed_file['passwd'])

menu = 'Menu:\n' \
       '1) Create group\n' \
       '2) Mailing to one group\n' \
       '3) Mailing to list of groups\n' \
       '4) Info about subscribers\n' \
       '5) List of subscribers filtered by "notification type"\n' \
       '* Type 1-5 to work with API\n' \
       '* Type "menu" to display the menu again\n' \
       '* Type "q" to exit\n'

print(menu)


while True:
    input_data = input('--> ')

    if input_data == 'menu':
        print('\n' + menu)

    if input_data == 'q':
        sys.exit()

    if input_data == '1':
        f = open('data.json', 'r')
        parsed_file = json.load(f)
        f.close()

        request = api.group_create(parsed_file['data'])
        corout = asyncio.run(request)
        print(corout, '\n')

    if input_data == '2':
        f = open('data.json', 'r')
        parsed_file = json.load(f)
        f.close()

        request = api.mailing_to_one_group(parsed_file['data'])
        corout = asyncio.run(request)
        print(corout, '\n')

    if input_data == '3':
        f = open('data.json', 'r')
        parsed_file = json.load(f)
        f.close()

        request = api.multiple_mailing(parsed_file['data'])
        corout = asyncio.run(request)
        print(corout, '\n')

    if input_data == '4':
        request = api.subscribers_info()
        corout = asyncio.run(request)
        print(corout, '\n')

    if input_data == '5':
        f = open('data.json', 'r')
        parsed_file = json.load(f)
        f.close()

        request = api.filter_by_notification_type(parsed_file['data'])
        corout = asyncio.run(request)
        print(corout, '\n')
