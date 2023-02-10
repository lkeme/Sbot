#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import os
from dataclasses import dataclass
from typing import Union

from app.adapter.core import get_bot
from app.adapter.events import MessageEvent
from app.adapter.message import AdapterMessageSegment
from app.config import config_mg
from app.logger import logger
from app.permission import ROLE
from app.plugin import plugin_mg as PM
from app.utils.draw import normal_image_draw
from app.utils.funcs import re_filter


@dataclass
class Config:
    # 插件基础信息
    name: str = '插件管理器插件'  # 插件名称
    path: str = 'plugin.default'  # 插件导入路径
    description: str = '插件管理器插件'  # 插件描述
    version: str = '0.0.1'  # 插件版本
    author: str = 'Lkeme'  # 插件作者
    data: bool = False  # 是否有外部资源
    # 插件配置
    enable: bool = False

    def __post_init__(self):
        self.enable = config_mg.get_bool(self.path, 'enable', appoint='plugin')


CONFIG: Union[Config, None] = None


def init_config():
    """
    初始化配置
    """
    config_mg.add(Config.path, 'enable', 'true', appoint='plugin')
    config_mg.save(appoint='plugin')
    #
    global CONFIG
    CONFIG = Config()


init_config()


def current_path(additional_path: str, resources: str) -> str:
    cp = os.path.abspath(os.path.dirname(__file__))
    return f"{cp}{os.sep}{additional_path}{os.sep}{resources}"


@PM.reg_event("message")
@re_filter("^重载插件$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def reload_plugins() -> None:
    bot = get_bot()
    await bot.register_plugins()


@PM.reg_event("message")
@re_filter("^插件列表$", role=ROLE.USER, enable=CONFIG.enable)
async def plugin_list(event: MessageEvent) -> None:
    bot = get_bot()
    content = await bot.plugin_format()
    await event.reply(content)


@PM.reg_event("message")
@re_filter("^启用插件 (.*?)$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def enable_plugin(event: MessageEvent) -> None:
    data = str(event.message).replace('启用插件 ', '').strip()
    bot = get_bot()
    content = await bot.plugin_format()
    if data not in content:
        return
    config_mg.set(data, 'enable', 'true', appoint='plugin')
    config_mg.save(appoint='plugin')

    await bot.register_plugins()


@PM.reg_event("message")
@re_filter("^禁用插件 (.*?)$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def disable_plugin(event: MessageEvent) -> None:
    data = str(event.message).replace('禁用插件 ', '').strip()
    bot = get_bot()
    content = await bot.plugin_format()
    if data not in content:
        return
    config_mg.set(data, 'enable', 'false', appoint='plugin')
    config_mg.save(appoint='plugin')

    await bot.register_plugins()


@PM.reg_event('message')
@re_filter("^plugin\?$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def plugin_help(event: MessageEvent):
    plain_text = """plugin? - 帮助 \n禁用插件 <插件名> - 停用插件 \n启用插件 <插件名> - 启用插件 \n重载插件 - 重新加载插件 \n插件列表 - 显示插件列表 \n"""
    try:
        pic = await normal_image_draw(plain_text)
        content = AdapterMessageSegment.image(pic)
        await event.reply(str(content))
    except Exception as e:
        logger.error(e)
