import aiohttp
import asyncio
import json

from copy import copy

API_URL = 'https://api.sendsay.ru'


class ManagerAPI:
    def __init__(self, login, password, api_url=API_URL, sublogin=None):
        self.login = login
        self.sublogin = sublogin or ''
        self.password = password
        self.api_url = api_url
        self.session = None

    async def aiohttp_request(self, data):
        async with aiohttp.ClientSession() as session:
            data = {
                'apiversion': 100,
                'json': 1,
                'request': json.dumps(data)
            }

            async with session.post(self.api_url, data=data) as response:
                data = await response.read()
                return json.loads(data)

    async def auth(self):
        data = {
            'action': 'login',
            'login': self.login,
            'sublogin': '',
            'passwd': self.password,
        }

        response = await self.aiohttp_request(data)
        self.session = response['session']

    async def request(self, action, params):
        if not self.session:
            await self.auth()

        request_params = copy(params)
        request_params['session'] = self.session
        request_params['action'] = action

        response = await self.aiohttp_request(request_params)
        return response

    async def group_create(self, params):  # создание группы со списком подписчиков (из файла)
        response = await self.request('group.create', params)

        if 'errors' in response:
            return response['errors']

        if not 'errors' in response:
            f = open('users.txt', 'r')
            lines = f.readlines()

            data = {
                'to': {
                    'id': params['id'],
                    'clean': 0
                },
                'from': {
                    'list': [line.rstrip('\n') for line in lines]
                }
            }

            response = await self.request('group.snapshot', data)
            return response

    async def mailing_to_one_group(self, params):  # запуск рассылки для одной группы
        response = await self.request('issue.send', params)

        return response

    async def multiple_mailing(self, params):  # запуск рассылки для списка групп (из файла)
        f = open('groups.txt', 'r')
        lines = f.readlines()

        for line in lines:  # асинхронный цикл не используется, т.к. при большом количестве групп можно случайно "задудосить" апи
            params['group'] = line.rstrip('\n')
            response = await self.request('issue.send', params)
            print(response)

            await asyncio.sleep(2)

        return 'ok'

    async def subscribers_info(self):  # информация о всех подписчиках; подписчики сгруппированы по типу уведомления
        subscribers_data = {}
        sub_types = ('email', 'msisdn', 'viber', 'csid', 'push', 'vk', 'tg')

        async def func(sub_type):
            response = await self.request('member.list', {'addr_type': sub_type})
            subscribers_data[sub_type] = response['list']

        tasks = [func(sub_type) for sub_type in sub_types]
        await asyncio.gather(*tasks)

        return subscribers_data

    async def filter_by_notification_type(self, params):  # вывод списка подписчиков по фильтру "тип уведомления"
        subscribers_data = {}

        response = await self.request('member.list', params)
        subscribers_data['sub_type'] = params['addr_type']
        subscribers_data['users'] = response['list']

        return subscribers_data
