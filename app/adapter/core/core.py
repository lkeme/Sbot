#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import asyncio
import importlib
import os
from collections import defaultdict as ddict
from types import ModuleType
from typing import Union, Coroutine, Any

from table2ascii import table2ascii, PresetStyle

from app.adapter import Adapter, AdapterConfig
from app.adapter.events import MessageEvent, NoticeEvent, RequestEvent, UnknownEvent
from app.adapter.events.meta import MetaEvent
from app.config import config_mg
from app.logger import logger
from app.plugin import plugin_mg
from app.utils.funcs import scheduler
from app.utils.path import create_path


class Core:
    """
    > 说明
        机器人实例类.
    > 参数
        + adapter [Adapter]: 适配器实例
    """

    def __init__(self) -> None:
        logger.info('Bot initialized.')
        #
        # self.cached_plugins = []
        self.loaded_modules: list = []
        self.plugins_loaded: bool = False
        self.plugins: list = []
        # 插件外部资源目录
        self.data_path: str = f".{os.sep}{config_mg.get('plugin', 'external')}{os.sep}"
        #
        self.adapter_config: AdapterConfig = self.set_adapter_config()
        self.adapter: Adapter = self.set_adapter()

        self.nickname = self.coroutine(self.adapter.nick_name)
        #
        logger.info('使用的适配器: `%s`.' % self.adapter.name)
        logger.info('登录成功: `%s`.' % self.nickname)

        # self.adapter_utils = self.adapter.utils

    def start_running(self) -> None:
        # 启动健康检查
        self.coroutine(self.adapter.check())
        # 启动Hook
        self.coroutine(self.hook_plugins())
        # 启动schedule
        scheduler.start()
        # 启动监听
        self.coroutine(self.adapter.start_listen())

    async def processor(self, data: dict) -> None:
        logger.info(data)

        self.ignore()
        msg = ddict(lambda: "unknown", data)
        switch, default = {
            "message": MessageEvent,
            "notice": NoticeEvent,
            "request": RequestEvent,
            "meta_event": MetaEvent,
        }, UnknownEvent
        event = switch.get(msg['post_type'], default)(self.adapter, msg, )
        logger.debug(event.fingerprint) if not event.fingerprint.startswith("u") else None
        await plugin_mg.broadcast(event)

    def set_adapter(self):
        return Adapter(
            adapter_config=self.adapter_config,
            auto_handle=self.processor,
        )

    @staticmethod
    def set_adapter_config() -> AdapterConfig:
        return AdapterConfig(
            http_token=config_mg.get('server', 'http_token'),
            http_host=config_mg.get('server', 'http_host'),
            http_port=config_mg.get_int('server', 'http_port'),
            http_protocol=config_mg.get('server', 'http_protocol'),
            ws_host=config_mg.get('server', 'ws_host'),
            ws_port=config_mg.get_int('server', 'ws_port'),
            ws_protocol=config_mg.get('server', 'ws_protocol'),
            ws_reverse=False if 'false' == config_mg.get('server', 'ws_reverse') else True,
        )

    async def hook_plugins(self):
        self.ignore()
        # boot
        await asyncio.gather(
            *[func() for func in plugin_mg.plugins['Boot']]
        )

    async def plugin_format(self, simplify=True) -> str:
        """
        插件列表
        """
        logger.info(self.plugins)
        default = 'Loading plugin: \n'
        body = []

        if simplify:
            for plugin in self.plugins:
                body.append([
                    plugin['path'], plugin['name'], plugin['version'], plugin['author'],
                    '√' if plugin['is_data'] else '×',
                    plugin['description'],
                    '√' if config_mg.get_bool(plugin['path'], 'enable', appoint='plugin') else '×',
                    plugin['remarks']
                ])

            output = table2ascii(
                header=["路径", "名称", "版本", "归属", "数据", "描述", "开关", "备注"],
                body=body,
                style=PresetStyle.ascii_box
            )
            return output if output else 'No plugin loaded.'
        else:
            for plugin in self.plugins:
                body.append([
                    plugin['path'], plugin['name'], plugin['version'], plugin['author'],
                    '√' if plugin['is_data'] else '×',
                    plugin['description'],
                    '√' if config_mg.get_bool(plugin['path'], 'enable', appoint='plugin') else '×',
                    plugin['remarks'], plugin['folder']
                ])

            output = table2ascii(
                header=["路径", "名称", "版本", "归属", "数据", "描述", "开关", "备注", "目录"],
                body=body,
                # column_widths=[10, 10, 10, 10, 10, 10, 10, 10, 10],
                style=PresetStyle.double_box
            )
            return f'{default}{output}' if output else 'No plugin loaded.'

    async def plugin_injection(self, plugin: dict, module: ModuleType) -> None:
        """
        插件注入
        """
        # plugin['remarks']
        plugin['name'] = module.CONFIG.name
        plugin['path'] = module.CONFIG.path
        plugin['version'] = module.CONFIG.version
        plugin['author'] = module.CONFIG.author
        plugin['is_data'] = module.CONFIG.data
        plugin['description'] = module.CONFIG.description
        plugin['enable'] = module.CONFIG.enable

        plugin['folder'] = self.data_path + (plugin['path']).replace('.', os.sep) + os.sep
        # 加入插件列表
        self.plugins.append(plugin)
        # 是否需要数据目录
        await self.register_plugin_data(plugin['is_data'], plugin['folder'])

    @staticmethod
    async def register_plugin_data(is_data: bool, path: str) -> None:
        """
        注册插件数据目录 No data directory required
        """
        if is_data:
            create_path(path)

    async def register_plugins(self, plugins: list = None):
        plugin_mg.plugins = ddict(list)  # clear plugins
        # 加载插件
        if self.plugins_loaded:  # reload plugins
            logger.info(f'reLoading plugins...')
            for i in self.loaded_modules:
                importlib.reload(i)
        else:  # load plugins
            for plugin in plugins:
                try:
                    # 完善插件路径
                    plugin['full_path'] = f"{config_mg.get('plugin', 'root')}.{plugin['path']}"
                    module = importlib.import_module(plugin['full_path'])
                    self.loaded_modules.append(module)
                    # 注入插件信息
                    await self.plugin_injection(plugin, module)
                except Exception as e:
                    logger.error(f"Loading plugin: {plugin['name']} -> {plugin['full_path']} -> {e}")
        logger.info(await self.plugin_format(False))
        self.plugins_loaded = True

    # def loop(self):
    #     logger.info("start Loop!")
    #
    #     # async def getMsg(websocket, path):
    #     #     while 1:
    #     #         msg = await websocket.recv()
    #     #         await self.processor(msg)
    #
    #     # handler
    #     async def get_message(websocket):
    #         async for msg in websocket:
    #             if not self.ws_connected:
    #                 self.ws_connected = True
    #                 logger.info("websocket client connected!")
    #             # logger.debug(msg)
    #             await self.processor(msg)
    #
    #     async def main():
    #         async with websockets.serve(
    #                 get_message,
    #                 config_mg.get('server', 'ws_host'),
    #                 config_mg.get_int('server', 'ws_port')
    #         ):
    #             await asyncio.Future()  # run forever
    #
    #     asyncio.run(main())

    # ignore Method '*' may be 'static'
    def ignore(self):
        ...

    @staticmethod
    def coroutine(coroutine: Union[Coroutine, Any]) -> Any:
        return asyncio.run(coroutine)
