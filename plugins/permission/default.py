#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import os
from dataclasses import dataclass
from typing import Union

from app.adapter import Group
from app.adapter.events import MessageEvent
from app.adapter.message import AdapterMessageSegment
from app.config import config_mg
from app.logger import logger
from app.permission import ROLE
from app.plugin import plugin_mg as PM
from app.utils.convert.convert import img2b64
from app.utils.draw import normal_image_draw
from app.utils.funcs import re_filter


@dataclass
class Config:
    # 插件基础信息
    name: str = '权限管理插件'  # 插件名称
    path: str = 'permission.default'  # 插件导入路径
    description: str = '权限管理插件'  # 插件描述
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
@re_filter("^重载配置$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def reload_config():
    config_mg.save(appoint='plugin')


# @PM.reg_event('message.private')
# @re_filter("^(get|add|rm)\ admin", role=ROLE.ADMIN, enable=CONFIG.enable)
# async def op_admin(event: MessageEvent):
#     if event.message.startswith("get"):
#         pass
#     elif event.message.startswith("add"):
#         try:
#             pass
#         except Exception as e:  # noqa
#             pass
#     elif event.message.startswith("rm"):
#         try:
#             pass
#         except Exception as e:  # noqa
#             pass


@PM.reg_event('message')
@re_filter(pattern="^群生效$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def group_effective(event: MessageEvent) -> None:
    if not isinstance(event.sender, Group):
        await event.reply("请在群内使用")
    else:
        valid_group = config_mg.get_list('permission', 'valid_group', appoint='plugin')
        valid_group.append(event.sender.group_id)
        config_mg.set('permission', 'valid_group', valid_group, appoint='plugin')
        config_mg.save(appoint='plugin')
        # 回复
        img = await img2b64(current_path('data', 'group_effective.gif'), True)
        content = AdapterMessageSegment.image(img)
        await event.reply(str(content))


@PM.reg_event('message')
@re_filter(pattern="^群失效$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def group_failure(event: MessageEvent) -> None:
    if not isinstance(event.sender, Group):
        await event.reply("请在群内使用")
    else:
        new_valid_group = []
        valid_group = config_mg.get_list('permission', 'valid_group', appoint='plugin')
        for group_id in valid_group:
            if group_id != event.sender.group_id:
                new_valid_group.append(group_id)
        config_mg.set('permission', 'valid_group', new_valid_group, appoint='plugin')
        config_mg.save(appoint='plugin')
        # 回复
        img = await img2b64(current_path('data', 'group_failure.gif'), True)
        content = AdapterMessageSegment.image(img)
        await event.reply(str(content))


@PM.reg_event('message')
@re_filter(pattern="^黑名单生效 (.*?)$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def blacklist_effective(event: MessageEvent) -> None:
    data = str(event.message).replace('黑名单生效 ', '').strip()
    if not data.isdigit():
        return
    else:
        target_id = int(data)
        blacklist = config_mg.get_list('permission', 'blacklist', appoint='plugin')
        blacklist.append(target_id)
        config_mg.set('permission', 'blacklist', blacklist, appoint='plugin')
        config_mg.save(appoint='plugin')


@PM.reg_event('message')
@re_filter(pattern="^黑名单失效 (.*?)$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def blacklist_failure(event: MessageEvent) -> None:
    data = str(event.message).replace('黑名单失效 ', '').strip()
    if not data.isdigit():
        return
    else:
        target_id = int(data)
        new_blacklist = []
        blacklist = config_mg.get_list('permission', 'blacklist', appoint='plugin')
        for black_id in blacklist:
            if black_id != target_id:
                new_blacklist.append(black_id)
        config_mg.set('permission', 'blacklist', new_blacklist, appoint='plugin')
        config_mg.save(appoint='plugin')


@PM.reg_event('message')
@re_filter(pattern="^白名单生效 (.*?)$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def whitelist_effective(event: MessageEvent) -> None:
    data = str(event.message).replace('白名单生效 ', '').strip()
    if not data.isdigit():
        return
    else:
        target_id = int(data)
        whitelist = config_mg.get_list('permission', 'whitelist', appoint='plugin')
        whitelist.append(target_id)
        config_mg.set('permission', 'whitelist', whitelist, appoint='plugin')
        config_mg.save(appoint='plugin')


@PM.reg_event('message')
@re_filter(pattern="^白名单失效 (.*?)$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def whitelist_failure(event: MessageEvent) -> None:
    data = str(event.message).replace('白名单失效 ', '').strip()
    if not data.isdigit():
        return
    else:
        target_id = int(data)
        new_whitelist = []
        whitelist = config_mg.get_list('permission', 'whitelist', appoint='plugin')
        for black_id in whitelist:
            if black_id != target_id:
                new_whitelist.append(black_id)
        config_mg.set('permission', 'whitelist', new_whitelist, appoint='plugin')
        config_mg.save(appoint='plugin')


@PM.reg_event('message')
@re_filter(pattern="^超级用户生效 (.*?)$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def superuser_effective(event: MessageEvent) -> None:
    data = str(event.message).replace('超级用户生效 ', '').strip()
    if not data.isdigit():
        return
    else:
        target_id = int(data)
        superuser = config_mg.get_list('permission', 'superuser', appoint='plugin')
        superuser.append(target_id)
        config_mg.set('permission', 'superuser', superuser, appoint='plugin')
        config_mg.save(appoint='plugin')


@PM.reg_event('message')
@re_filter(pattern="^超级用户失效 (.*?)$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def superuser_failure(event: MessageEvent) -> None:
    data = str(event.message).replace('超级用户失效 ', '').strip()
    if not data.isdigit():
        return
    else:
        target_id = int(data)
        new_superuser = []
        superuser = config_mg.get_list('permission', 'superuser', appoint='plugin')
        for black_id in superuser:
            if black_id != target_id:
                new_superuser.append(black_id)
        config_mg.set('permission', 'superuser', new_superuser, appoint='plugin')
        config_mg.save(appoint='plugin')


@PM.reg_event('message')
@re_filter("^permission\?$", role=ROLE.ADMIN, enable=CONFIG.enable)
async def permission_help(event: MessageEvent):
    plain_text = """permission? - 帮助 \n超级用户失效 <id> - 移除超级用户 \n超级用户生效 <id> - 添加超级用户 \n白名单失效 <id> - 移除白名单用户 \n白名单生效 <id> - 添加白名单用户 \n黑名单失效 <id> - 移除黑名单用户 \n黑名单生效 <id> - 添加黑名单用户 \n群生效 - 添加生效群 \n群失效 - 移除生效群 \n重载配置 - 重载配置文件 \n"""
    try:
        pic = await normal_image_draw(plain_text)
        content = AdapterMessageSegment.image(pic)
        await event.reply(str(content))
    except Exception as e:
        logger.error(e)
