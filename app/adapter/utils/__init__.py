#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from collections import defaultdict as ddict
from typing import Union

from aiohttp import request, ClientConnectorError

from app.logger import logger
from ..contact import Friend, Group, Member


class AdapterUtils:
    def __init__(self, adapter) -> None:
        self.http_token = adapter.http_token
        self.host = adapter.http_host
        self.port = adapter.http_port
        self.protocol = adapter.http_protocol

    def get_http_server(self, api_path: str) -> str:
        return '%s%s:%s%s' % (self.protocol, self.host, self.port, api_path)

    async def send_msg(self, params: dict, api_path: str) -> dict:
        return await self.request_api(f"/send_{api_path}_msg", params=params, data=False, method='POST')

    async def get_status(self) -> dict:
        return await self.request_api('/get_status')

    async def get_login_info(self) -> dict:
        return await self.request_api('/get_login_info')

    async def request_api(self, path: str, data: bool = True, params: dict = None, method: str = 'GET') -> dict:
        try:
            url = self.get_http_server(path)
            params = ddict(lambda: None, params if params else {})
            # params = params if params else {}
            if not params['access_token']:
                params['access_token'] = self.http_token
            if not path.startswith('/'):
                logger.error("terminal must be like '/xxxx' !!!")
            if method == 'GET':
                async with request('GET', url, params=params) as response:
                    _ = await response.json()
                    logger.debug(f"{response.ok}->{response.status}->{_}")
                    return _['data'] if data else _
            else:
                del params['access_token']
                # f'{url}?access_token={self.http_token}'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.http_token}',
                }
                async with request('POST', url, json=params, headers=headers) as response:
                    _ = await response.json()
                    logger.debug(f"{response.ok}->{response.status}->{_}")
                    return _['data'] if data else _

        except ClientConnectorError:
            raise ConnectionError('无法连接到 CQHTTP 服务, 请检查是否配置完整!')

    async def get_friend_by_id(self, user_id: int) -> Friend:
        for i in await self.request_api('/get_friend_list'):
            if i['user_id'] == user_id:
                return Friend(i['user_id'], i['nickname'], i['remark'])
        logger.error('无法找到好友 `%s`!' % user_id)

    async def get_group_by_id(self, group_id: int) -> Group:
        for i in await self.request_api('/get_group_list'):
            if i['group_id'] == group_id:
                return Group(i['group_id'], i['group_name'], i['max_member_count'], i['member_count'],
                             i['group_level'], i['group_create_time'])
        logger.error('无法找到群 `%s`!' % group_id)

    async def get_member_by_id(self, group_id: int, user_id: int) -> Member:
        data = await self.request_api(f'/get_group_member_list', data=False, params={'group_id': group_id})
        if data['retcode'] == 100:
            logger.error('%s: `%s`!' % (data['wording'], user_id))
        else:
            for i in data['data']:
                if i['user_id'] == user_id:
                    return Member(await self.get_group_by_id(group_id), i['user_id'], group_id, i['nickname'],
                                  i['role'],
                                  i['last_sent_time'], i['join_time'])
            logger.error('无法找到群成员 `%s:%s`!' % (group_id, user_id))

    async def get_forward_message(self, id: str) -> Union[dict, None]:
        return await self.request_api(f'/get_forward_msg', data=True, params={'id': id})

    async def get_message_by_id(self, message_id: int) -> Union[dict, None]:
        """
        获取消息
        """
        return await self.request_api(f'/get_msg', data=True, params={'message_id': message_id})

    async def get_version_info(self) -> Union[dict, None]:
        """
        获取版本信息
        """
        return await self.request_api(f'/get_version_info')
