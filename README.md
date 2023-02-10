# SBot

基于 [GO-CQHTTP](https://docs.go-cqhttp.org/) 协议开发的 QQ 功能型机器人

## 安装依赖

pip install -r requements.txt

## 内置插件

+ [x] 基础插件
+ [x] 权限管理插件
+ [x] 插件管理器插件
+ [x] ChatGPT插件
+ [x] Warframe插件
+ [x] 二维码编码解码插件
+ [x] 权重查询插件
+ [x] ...

## 实现插件

### 1. 加载插件

```python
"""
修改文件 main.py
path: 插件路径 (string) 对应 plugins 文件夹下的文件夹路径 plugins/example/default.py
name: 插件名称 (string) 用于显示在控制台
data: 是否需要数据目录 (bool) 用于创建数据目录  resources/plugins/example/default/*
"""
plugins = [
    # {'path': '路径(string)', 'remarks': '名称(string)'}, # 例子毋删
    {'path': 'example.default', 'remarks': '示例插件'},
]
```

### 2. 开发插件

```python
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
from app.utils.funcs import cron, scheduler
from app.utils.funcs import re_filter

section = 'base.default'


@dataclass
class Config:
    enable: bool = False

    def __post_init__(self):
        self.enable = config_mg.get_bool(section, 'enable', appoint='plugin')


CONFIG: Union[Config, None] = None


def init_config():
    """
    初始化配置
    """
    config_mg.add(section, 'enable', 'true', appoint='plugin')
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
    ● 启动时间：{DASH_PANEL.bot_start_time()} \n\
    ● 运行时间：{DASH_PANEL.bot_running_time()}"

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

```

### 3. 插件定时任务

```python
from app.plugin import plugin_mg as PM
from app.utils.funcs import cron, scheduler


@PM.reg_event('scheduler')
@scheduler.scheduled_job(cron(hour=22, minute=2))
async def example():
    pass
```

### 4. 注册插件

```python
from app.plugin import plugin_mg as PM

"""
不同装饰器参数对应不同的消息类型，遇到该事件类型会对应触发该对应函数
"""


@PM.reg_event('message')
@PM.reg_event('message.group')
@PM.reg_event('message.private')
async def test():
    pass

```

### 5. 触发函数

```python
from app.permission import ROLE
from app.utils.funcs import re_filter

"""
参数1: 触发正则表达式
参数2: 触发角色，可选值 ROLE.SU, ROLE.USER, ROLE.ADMIN..
参数3: 是否启用, 根据CONFIG.enable的值来决定是否启用
"""


@re_filter("^test private reply$", role=ROLE.USER, enable=True)
async def test():
    pass
```

### 6. 框架概念

#### Event（事件）

1. message包括 private 私聊消息 和 group 群聊消息
2. notice包括 群文件上传 群成员增加/减少
3. request包括 新朋友 和 进群邀请
4. meta
5. unknown (考虑到未来的兼容性)

#### 额外

    > 参考plugins/base/default.py的内容进行开发

- PM.reg_event(fingerprint)

- 接受指纹作为参数 装饰插件函数，当遇到具有该指纹类型的事件的时候，函数会被触发

- re_filter(pattern)

- 根据正则表达式进行过滤，只有通过过滤的消息才会触发函数

- get_bot()

- 获取bot实例，用于编写涉及到bot层的插件。