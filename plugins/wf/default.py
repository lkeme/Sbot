#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import asyncio
import json
import os
import re
import time
from dataclasses import dataclass
from typing import Union
from urllib.parse import quote

from bs4 import BeautifulSoup

from app.adapter.core import get_bot
from app.adapter.events import MessageEvent
from app.adapter.message import AdapterMessageSegment
from app.config import config_mg
from app.logger import logger
from app.permission import ROLE
from app.plugin import plugin_mg as PM
from app.request import request
from app.utils.draw import normal_image_draw
from app.utils.funcs import re_filter


@dataclass
class Config:
    # 插件基础信息
    name: str = 'Warframe插件'  # 插件名称
    path: str = 'wf.default'  # 插件导入路径
    description: str = 'Warframe插件'  # 插件描述
    version: str = '0.0.1'  # 插件版本
    author: str = 'Lkeme'  # 插件作者
    data: bool = True  # 是否有外部资源
    # 插件配置
    enable: bool = False

    def __post_init__(self):
        self.enable = config_mg.get_bool(self.path, 'enable', appoint='plugin')


CONFIG: Union[Config, None] = None


def init_config():
    """
    初始化配置
    """
    config_mg.add(Config.path, 'enable', 'false', appoint='plugin')
    config_mg.save(appoint='plugin')
    #
    global CONFIG
    CONFIG = Config()


init_config()


async def check_warframe_price(commodity: str) -> Union[str, None]:
    """
    查询价格
    https://github.com/WsureWarframe/warframe-info-api
    """
    url = f'http://nymph.rbq.life:3000/wm/robot/{quote(commodity)}'
    logger.debug(f'Fetch check_warframe_price {url}')
    try:
        rsp = await request.get(url, stream=True, timeout=20)
        if 200 == rsp.status_code:
            return await rsp.text
        logger.error(f'Failed check_warframe_price {url}. HTTP {rsp.status_code}')
    except Exception as e:
        logger.error(f'Failed check_warframe_price {url}. {type(e)}')
        logger.exception(e)
    return None  # error


@PM.reg_event('message')
@re_filter("^wm (.*?)$", role=ROLE.USER, enable=CONFIG.enable)
async def wm(event: MessageEvent) -> None:
    data = str(event.message).replace('wm ', '').strip()
    # noinspection PyBroadException
    try:
        html = await check_warframe_price(data)
        if html == '' or html is None:
            raise Exception('查询错误或结果为空')
        pic = await normal_image_draw(html)
        content = AdapterMessageSegment.image(pic)
        await event.reply(str(content))
    except Exception as e:
        logger.error(e)


async def check_riven_price(commodity: str) -> Union[str, None]:
    """
    查询紫卡价格
    https://github.com/WsureWarframe/warframe-info-api
    """
    url = f'http://nymph.rbq.life:3000/rm/robot/{quote(commodity)}'
    logger.debug(f'Fetch check_riven_price {url}')
    try:
        rsp = await request.get(url, stream=True, timeout=20)
        if 200 == rsp.status_code:
            return await rsp.text
        logger.error(f'Failed check_riven_price {url}. HTTP {rsp.status_code}')
    except Exception as e:
        logger.error(f'Failed check_riven_price {url}. {type(e)}')
        logger.exception(e)
    return None  # error


@PM.reg_event('message')
@re_filter("^rm (.*?)$", role=ROLE.USER, enable=CONFIG.enable)
async def rm(event: MessageEvent) -> None:
    data = str(event.message).replace('rm ', '').strip()
    # noinspection PyBroadException
    try:
        html = await check_riven_price(data)
        if html == '' or html is None:
            raise Exception('查询错误或结果为空')
        pic = await normal_image_draw(html)
        content = AdapterMessageSegment.image(pic)
        await event.reply(str(content))
    except Exception as e:
        logger.error(e)


async def check_warframe_state(commodity: str) -> Union[str, None]:
    """
    查询世界状态
    https://github.com/WsureWarframe/warframe-info-api
    """
    url = f'http://nymph.rbq.life:3000/wf/robot/{quote(commodity)}'
    logger.debug(f'Fetch check_warframe_state {url}')
    try:
        rsp = await request.get(url, stream=True, timeout=20)
        if 200 == rsp.status_code:
            return await rsp.text
        logger.error(f'Failed check_warframe_state {url}. HTTP {rsp.status_code}')
    except Exception as e:
        logger.error(f'Failed check_warframe_state {url}. {type(e)}')
        logger.exception(e)
    return None  # error


@PM.reg_event('message')
@re_filter("^wf (.*?)$", role=ROLE.USER, enable=CONFIG.enable)
async def wf(event: MessageEvent) -> None:
    maps = {
        "timestamp": "服务器时间",
        "news": "新闻",
        "events": "活动",
        "alerts": "警报",
        "sortie": "突击",
        "Ostrons": "地球赏金",
        "Solaris": "金星赏金",
        "EntratiSyndicate": "火卫二赏金",
        "fissures": "裂缝",
        "flashSales": "促销商品",
        "invasions": "入侵",
        "voidTrader": "奸商",
        "dailyDeals": "达尔沃",
        "persistentEnemies": "小小黑",
        "earthCycle": "地球",
        "cetusCycle": "地球平原",
        "constructionProgress": "舰队",
        "vallisCycle": "金星平原",
        "nightwave": "电波",
        "arbitration": "仲裁",
        "cambionCycle": "火卫二平原",
        "zarimanCycle": "扎里曼"
    }
    data = str(event.message).replace('wf ', '').strip()

    for k, v in maps.items():
        if v == data:
            # noinspection PyBroadException
            try:
                html = await check_warframe_state(k)
                if html == '' or html is None:
                    raise Exception('查询错误或结果为空')
                pic = await normal_image_draw(html)
                content = AdapterMessageSegment.image(pic)
                await event.reply(str(content))
            except Exception as e:
                logger.error(e)
            return
    else:
        return


async def parse_warframe_list(html: str) -> list:
    """
    解析战甲列表
    """
    soup = BeautifulSoup(html, features='html.parser')
    tables = soup.findAll(attrs={"class": 'primewf'})
    return [table.find("img").attrs['alt'] for table in tables]


async def get_warframe_list() -> Union[str, None]:
    """
    获取战甲列表
    """
    url = 'https://www.warframe.com/zh-hans/game/warframes'
    logger.debug(f'Fetch warframe list {url}')
    try:
        rsp = await request.get(url, stream=True, timeout=20)
        if 200 == rsp.status_code:
            return await rsp.text
        logger.error(f'Failed to fetch {url}. HTTP {rsp.status_code}')
    except Exception as e:
        logger.error(f'Failed to fetch {url}. {type(e)}')
        logger.exception(e)
    return None  # error


# 离线版本
async def offline_fetch(path: str) -> str:
    with open(path, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    # if json_data['ts'] + 3600 * 2 < time.time():
    #     os.remove(path)
    new_data = ''
    for j in json_data['list']:
        new_data += f"{j['name']} => 昨日均价: {j['yesterday']}p => 估价区间: {j['range']}\n"

    return new_data


# 解析价格
async def parse_price(name: str, html) -> dict:
    # noinspection PyBroadException
    try:
        y = re.search('昨日均价：(.*?)p\n', html).group(1)
        if '.' in y:
            y = int(float(y))
        else:
            y = int(y)
        return {
            'name': name,
            'yesterday': y,
            'range': re.search('估计价格区间：(.*?)\n', html).group(1),
        }
    except Exception as e:
        logger.error(e)
        return {
            'name': name,
            'yesterday': 0,
            'range': '* - *',
        }


# 在线版本
async def online_fetch(path: str) -> Union[str, None]:
    # 拉取
    warframe_list_data = await get_warframe_list()
    if warframe_list_data is None or warframe_list_data == '':
        return ''
    # 解析
    warframe_list = await parse_warframe_list(warframe_list_data)
    if warframe_list is None or warframe_list == []:
        return ''
    # 查价
    new_list = []
    new_dict = {'ts': int(time.time()), 'list': []}
    for warframe in warframe_list:
        html = await check_warframe_price(warframe)
        j = await parse_price(warframe, html)
        new_list.append(j)
        await asyncio.sleep(0.5)
    # 排序
    new_list.sort(key=lambda d: int(d['yesterday']))
    new_dict['list'] = new_list

    with open(path, 'w', encoding='utf-8') as fw:
        json.dump(new_dict, fw, indent=4, ensure_ascii=False)


@PM.reg_event('message')
@re_filter("^wfs$", role=ROLE.USER, enable=CONFIG.enable)
async def wfs(event: MessageEvent) -> None:
    bot = get_bot()
    path = f'{bot.data_path}wf{os.sep}default{os.sep}warframe_list.json'
    # noinspection PyBroadException
    try:
        if not os.path.exists(path):
            # noinspection PyBroadException
            try:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf8') as fp:
                        json_data = json.load(fp)
                    if json_data['ts'] + 3600 * 2 < int(time.time()):
                        await online_fetch(path)
                else:
                    await online_fetch(path)
            except Exception as e:
                logger.error(e)

        content = await offline_fetch(path)
        pic = await normal_image_draw(content)
        content = AdapterMessageSegment.image(pic)
        await event.reply(str(content))
    except Exception as e:
        logger.error(e)


@PM.reg_event('message')
@re_filter("^wf\?$", role=ROLE.USER, enable=CONFIG.enable)
async def wf_help(event: MessageEvent):
    plain_text = """wf? - 帮助 \nwf <地图与杂项> - 查询世界状态 \nwm <物品名> - 查询物品价格 \nrm <紫卡名称> - 查询紫卡价格 \nwfs - 查询所有战甲价格 \n"""
    try:
        pic = await normal_image_draw(plain_text)
        content = AdapterMessageSegment.image(pic)
        await event.reply(str(content))
    except Exception as e:
        logger.error(e)
