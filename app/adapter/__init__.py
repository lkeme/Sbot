#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import asyncio
import json
from abc import ABCMeta, abstractmethod
from typing import Any, Union
from typing import Coroutine

import nest_asyncio
import websockets
from overrides import overrides

from app.logger import logger
from .config import AdapterConfig
from .contact import Contact, Group, Friend
# from .handler import MessageHandler, EventHandler
from .utils import AdapterUtils

nest_asyncio.apply()


class BaseAdapter(metaclass=ABCMeta):
    """
    > 说明
        适配器基类，用于实现适配器模式.
    """

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def check(self) -> None:
        ...

    @abstractmethod
    def login_info(self) -> dict:
        ...

    @abstractmethod
    def nick_name(self) -> str:
        ...

    @abstractmethod
    async def start_listen(self) -> Any:
        ...


class Adapter(BaseAdapter):
    """
    > 说明
        CQHTTP 适配器.
    > 参数
        + config [AdapterConfig]: 适配器对应的配置对象
    """

    def __init__(self, adapter_config: AdapterConfig, auto_handle: callable) -> None:
        self.name = 'CQHTTP'
        # Message\Event SETTING
        self.auto_handle = auto_handle
        # HTTP API SETTING
        self.http_token = adapter_config.http_token
        self.http_host = adapter_config.http_host
        self.http_port = adapter_config.http_port
        self.http_protocol = adapter_config.http_protocol
        # WS API SETTING
        self.ws_host = adapter_config.ws_host
        self.ws_port = adapter_config.ws_port
        self.ws_protocol = adapter_config.ws_protocol
        self.ws_reverse = adapter_config.ws_reverse
        #
        self.utils = AdapterUtils(self)
        #
        # self.message_handler = MessageHandler(self)
        # self.event_handler = EventHandler(self)
        self.websocket = None

    def get_ws_server(self) -> str:
        return '%s%s:%s' % (self.ws_protocol, self.ws_host, self.ws_port)

    @overrides
    async def check(self) -> None:
        if not (await self.utils.get_status())['online']:
            raise ConnectionError('尝试连接 CQHTTP 时返回了一个错误的状态, 请尝试重启 CQHTTP!')

    # @overrides
    # async def check(self) -> bool:
    #     """
    #     # https://docs.go-cqhttp.org/api/#获取状态
    #     # https://docs.go-cqhttp.org/api/#获取版本信息
    #     # https://docs.go-cqhttp.org/api/#获取运行时信息
    #     """
    #     while True:
    #         # noinspection PyBroadException
    #         try:
    #             logger.debug("waiting for online...")
    #             if (await self._request_api('/get_status'))['online']:
    #                 return True
    #         except Exception as e:
    #             # if not (await self._request_api('/get_status'))['online']:
    #             #     raise ConnectionError('尝试连接 CQHTTP 时返回了一个错误的状态, 请尝试重启 CQHTTP!')
    #             logger.debug('尝试连接 CQHTTP 时返回了一个错误的状态, 请尝试重启 CQHTTP!')
    #             await asyncio.sleep(1)

    @property
    async def login_info(self) -> dict:
        return await self.utils.get_login_info()

    @property
    async def nick_name(self) -> str:
        return (await self.login_info)['nickname']

    @overrides
    async def start_listen(self) -> Any:
        try:
            coroutine = await self.__reverse_listen() \
                if self.ws_reverse else await self.__obverse_listen()
            logger.info(coroutine)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(coroutine)
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info('已退出!')

    async def __obverse_listen(self) -> Coroutine:
        async def run():
            with logger.console.status('正在尝试连接至 %s WebSocket 服务器...' % self.name) as status:
                async with websockets.connect(
                        self.get_ws_server()
                ) as self.websocket:
                    logger.info('正向WS连接成功, 开始监听消息!')
                    status.stop()
                    while True:
                        data = json.loads(await self.websocket.recv())
                        await self.auto_handle(data)

        return run()

    async def __reverse_listen(self) -> Coroutine:
        async def run():
            with logger.console.status('正在等待 WebSocket 客户端连接...') as status:
                self.is_stopped = False

                async def handle(websocket: websockets.WebSocketServerProtocol, path):
                    self.websocket = websocket
                    async for message in self.websocket:
                        if not self.is_stopped:
                            logger.info('反向WS连接成功, 开始监听消息!')
                            status.stop()
                            self.is_stopped = True
                        data = json.loads(message)
                        await self.auto_handle(data)

                async with websockets.serve(handle, self.ws_host, self.ws_port):
                    logger.info('WebSocket 服务器建立成功: %s%s:%s' % (
                        self.ws_protocol, self.ws_host, self.ws_port))
                    while True:
                        await asyncio.Future()

        return run()

    # async def auto_handle(self, data: dict) -> None:
    #     _type = data['post_type']
    #     if _type == 'message':
    #         await self.message_handler.handle(data)
    #     else:
    #         await self.event_handler.handle(data)

    async def send_message(self, target: Union[Contact, Friend, Group], message: str) -> Any:
        is_friend = isinstance(target, Friend)
        t = ('user_id' if is_friend else 'group_id',
             target.user_id if is_friend else target.group_id,
             'private' if is_friend else 'group',
             (await self.utils.get_friend_by_id(target.user_id)).nickname
             if is_friend else (await self.utils.get_group_by_id(target.group_id)).group_name)
        data = {t[0]: t[1], 'message': message}
        response = await self.utils.send_msg(data, t[2])
        if response['retcode'] != 0:
            logger.error(f"发送消息失败: 状态码错误. 返回结果: {response['wording']}.")
        else:
            logger.info('%s\n -> %s(%s)' % (message[:50], t[3], t[1]))
