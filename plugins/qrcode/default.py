#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme
import os
import re
from io import BytesIO
from typing import Union

from PIL import Image

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
from app.utils.convert.convert import img2b64


@dataclass
class Config:
    # 插件基础信息
    name: str = '二维码编解码'  # 插件名称
    path: str = 'qrcode.default'  # 插件导入路径
    description: str = '二维码编解码'  # 插件描述
    version: str = '0.0.1'  # 插件版本
    author: str = 'Lkeme'  # 插件作者
    data: bool = False  # 是否有外部资源
    # 插件配置
    enable: bool = True

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


def get_reply_images(message: str) -> Union[list, None]:
    """
    获取回复图片
    """
    ret = re.findall(r"\[CQ:image,file=.*?,url=(.*?)\]", message)
    if ret:
        return ret
    return None


async def get_universal_img_url(url: str) -> str:
    """
    获取通用图片链接
    """
    final_url = url.replace(
        "/c2cpicdw.qpic.cn/offpic_new/", "/gchat.qpic.cn/gchatpic_new/"
    )
    final_url = re.sub(r"/\d+/+\d+-\d+-", "/0/0-0-", final_url)
    final_url = re.sub(r"\?.*$", "", final_url)

    rsp = await request.get(final_url, stream=True, timeout=20)
    if rsp.status_code == 200:
        return final_url
    return url


async def get_image_content(url: str) -> bytes:
    """
    获取图片内容
    """
    rsp = await request.get(url, stream=True, timeout=20)
    if rsp.status_code == 200:
        return await rsp.content
    return b''


async def decode_qrcode(content: bytes) -> str:
    """
    解析二维码
    """
    try:
        return str(pyzbar.decode(Image.open(BytesIO(content)), symbols=[pyzbar.ZBarSymbol.QRCODE])[0][0],
                   encoding="utf-8")
    except Exception as e:
        return str(e)
    # img = Image.open(BytesIO(content))
    # result = pyzbar.decode(img)
    # if result:
    #     return f"解析结果：{result[0].data.decode('utf-8')}\n"
    # return ""


async def encode_qrcode(content: str,
                        optimize_level: int = 20,
                        error_correction: int = qrcode_qrcode.constants.ERROR_CORRECT_M,
                        box_size: int = 10,
                        border: int = 4) -> bytes:
    """
    error_correction:控制二维码纠错级别。
    ERROR_CORRECT_L:大约7%或者更少的错误会被更正。
    ERROR_CORRECT_M:默认值，大约15%或者更少的错误会被更正。
    ERROR_CORRECT_Q:大约25%或者更少的错误会被更正。
    ERROR_CORRECT_H:大约30%或者更少的错误会被更正。
    box_size:控制二维码中每个格子的像素数，默认为10。
    border:控制二维码四周留白包含的格子数，默认为4。
    image_factory:选择生成图片的形式，默认为PIL图像。
    mask_pattern:选择生成图片的的掩模。

 """
    qr = qrcode_qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border)
    qr.add_data(content, optimize=optimize_level)
    qr.make()

    im = qr.make_image().get_image()

    img_byte = BytesIO()
    im.save(img_byte, format='png')
    binary_content = img_byte.getvalue()
    img_byte.close()

    return binary_content


@PM.reg_event('message')
@re_filter("^qrcode(.*?)", enable=CONFIG.enable)
async def qrcode(event: MessageEvent) -> None:
    data = str(event.message).replace('qrcode', '').strip()
    reply_images = get_reply_images(data)
    if not reply_images:
        # 编码
        img = await encode_qrcode(data)
        image = await img2b64(img)
        message = AdapterMessageSegment.image(image)
        logger.info(message)
    else:
        # 解码
        message = ""
        for i in reply_images:
            url = await get_universal_img_url(i)
            content = await get_image_content(url)
            message += await decode_qrcode(content)
    if message:
        await event.reply(str(message))


@PM.reg_event('message')
@re_filter("^qrcode\?$", enable=CONFIG.enable)
async def qrcode_help(event: MessageEvent):
    plain_text = """qrcode? - 帮助 - User↑\nqrcode <内容/图片> - 请求答复内容 - User↑\n"""
    try:
        pic = await normal_image_draw(plain_text)
        content = AdapterMessageSegment.image(pic)
        await event.reply(str(content))
    except Exception as e:
        logger.error(e)
