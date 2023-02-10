#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme
import os
import re
from typing import Union

from app.adapter.message import AdapterMessageSegment
from app.config import config_mg
from app.logger import logger

try:
    import qrcode as qrcode_qrcode
except Exception as _:  # noqa
    os.system('pip install qrcode -i https://pypi.tuna.tsinghua.edu.cn/simple')
    import qrcode as qrcode_qrcode
try:
    import pyzbar.pyzbar as pyzbar
except Exception as _:  # noqa
    os.system('pip install pyzbar -i https://pypi.tuna.tsinghua.edu.cn/simple')
    import pyzbar.pyzbar as pyzbar
from app.request import request
from app.adapter.events import MessageEvent
from app.plugin import plugin_mg as PM
from app.utils.funcs import re_filter
from dataclasses import dataclass
from app.utils.draw import normal_image_draw


@dataclass
class Config:
    # 插件基础信息
    name: str = 'QQ权重查询'  # 插件名称
    path: str = 'weight.default'  # 插件导入路径
    description: str = 'QQ权重查询'  # 插件描述
    version: str = '0.0.1'  # 插件版本
    author: str = 'Lkeme'  # 插件作者
    data: bool = False  # 是否有外部资源
    # 插件配置
    enable: bool = True  # 是否启用

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


async def get_api_content(qq: str) -> str:
    """
    获取api内容
    """
    url = f'http://tc.tfkapi.top/API/qqqz.php?qq={qq}'

    rsp = await request.get(url, stream=True, timeout=20)
    if rsp.status_code == 200:
        return await rsp.text
    return ''


def get_reply_ats(message: str) -> Union[list, None]:
    """
    获取at
    """
    ret = re.findall(r"\[CQ:at,qq=(\d+)", message)
    if ret:
        return ret
    return None


@PM.reg_event('message')
@re_filter("^权重(.*?)", enable=CONFIG.enable)
async def weight(event: MessageEvent) -> None:
    data = str(event.message).replace('权重', '').strip()
    reply_ats = get_reply_ats(data)
    message: str = ''
    if reply_ats:
        for reply_at in reply_ats:
            content = await get_api_content(reply_at)
            message = f'账号:{reply_at} {content}'
    else:
        content = await get_api_content(str(event.sender_id))
        message = f'账号:{event.sender_id} {content}'
    if message:
        await event.reply(message)


@PM.reg_event('message')
@re_filter("^weight\?$", enable=CONFIG.enable)
async def weight_help(event: MessageEvent):
    plain_text = """weight? - 帮助 - User↑\nweight <内容/at> - 请求答复内容 - User↑\n"""
    try:
        pic = await normal_image_draw(plain_text)
        content = AdapterMessageSegment.image(pic)
        await event.reply(str(content))
    except Exception as e:
        logger.error(e)
