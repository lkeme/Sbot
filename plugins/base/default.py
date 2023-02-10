#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import os
from dataclasses import dataclass
from typing import Union

from app.adapter import Friend
from app.adapter.actions import MessageAction
from app.adapter.core import get_bot
from app.adapter.events import MessageEvent
from app.adapter.message import AdapterMessageSegment
from app.config import config_mg
from app.logger import logger
from app.permission import ROLE
from app.plugin import plugin_mg as PM
from app.request import request
from app.utils.convert.convert import img2b64
from app.utils.draw import normal_image_draw
from app.utils.funcs import cron, scheduler
from app.utils.funcs import re_filter


@dataclass
class Config:
    # 插件基础信息
    name: str = '默认插件'  # 插件名称
    path: str = 'base.default'  # 插件导入路径
    description: str = '默认插件'  # 插件描述
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


@PM.reg_event('message')
@re_filter(pattern="^状态$", role=ROLE.SU, enable=CONFIG.enable)
async def status(event: MessageEvent) -> None:
    from bootstrap import DASH_PANEL
    response = await event.ma.adapter.utils.get_version_info()
    stat_str = f"当前状态： \n\n\
    ● 应用版本：{response['app_version']} \n\
    ● 协议类型：{response['protocol_name']} \n\
    ● 协议版本：{response['protocol_version']} \n\
    ● 系统环境：{response['runtime_os']} \n\
    ● 系统版本：{response['runtime_version']} \n\
    ● 内存状态：{await DASH_PANEL.memory_status()} \n\
    ● CPU状态： {await DASH_PANEL.cpu_status()} \n\
    ● 硬盘状态：{await DASH_PANEL.disk_status()} \n\
    ● 启动时间：{await DASH_PANEL.bot_start_time()} \n\
    ● 运行时间：{await DASH_PANEL.bot_running_time()}"

    await event.reply(stat_str)


@PM.reg_event('message')
@re_filter("^ping$", role=ROLE.SU, enable=CONFIG.enable)
async def ping(event: MessageEvent):
    await event.reply("pong")


@PM.reg_event('message.group')
@re_filter("^test group reply$", role=ROLE.USER, enable=CONFIG.enable)
async def reply_me(event: MessageEvent):
    await event.reply("just replied", True)


@PM.reg_event('message.private')
@re_filter("^test private reply$", role=ROLE.USER, enable=CONFIG.enable)
async def reply_me(event: MessageEvent):
    await event.reply("just replied", True)


# @PM.reg_event("Boot")
# async def hello():
#     bot = get_bot()
#     image = await img2b64(current_path('data', 'hello.gif'), True)
#     content = AdapterMessageSegment.image(image)
#     target_id = config_mg.get_int('permission', 'admin', appoint='plugin')
#     await MessageAction(bot.adapter).send_msg(Friend(user_id=target_id), str(content))


async def __moyu():
    url = 'https://api.vvhan.com/api/moyu'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    logger.debug(f'Fetch check_warframe_price {url}')
    try:
        rsp = await request.get(url, headers=headers, stream=True, timeout=20)
        if 200 == rsp.status_code:
            return await rsp.content
        logger.error(f'Failed check_warframe_price {url}. HTTP {rsp.status_code}')
    except Exception as e:
        logger.error(f'Failed check_warframe_price {url}. {type(e)}')
        logger.exception(e)
    return None  # error'


@PM.reg_event('scheduler')
@scheduler.scheduled_job(cron(hour=22, minute=2))
async def moyu():
    bot = get_bot()
    img = await __moyu()
    pic = await img2b64(img)
    content = AdapterMessageSegment.image(pic)
    target_id = config_mg.get_int('permission', 'admin', appoint='plugin')
    await MessageAction(bot.adapter).send_msg(Friend(user_id=target_id), str(content))


@PM.reg_event('message')
@re_filter("^base\?$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def base_help(event: MessageEvent):
    plain_text = """base? - 帮助 \n状态 - Bot状态 \nping - 响应测试 \ntest group reply - 测试群回复 \ntest private reply - 测试私信回复 \n"""
    try:
        pic = await normal_image_draw(plain_text)
        content = AdapterMessageSegment.image(pic)
        await event.reply(str(content))
    except Exception as e:
        logger.error(e)
