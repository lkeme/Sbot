#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from app.logger import logger
from .. import Adapter
from ..contact import Contact


class MessageAction:
    """
    > 说明
        机器人实例类.
    > 参数
        + adapter [Adapter]: 适配器实例
    """

    def __init__(self, adapter: Adapter) -> None:
        self.adapter = adapter

    async def send_msg(self, target: Contact, message: str) -> None:
        """
        > 说明
            向联系人发送消息.
        > 参数
            + target [Contact]: 联系人实例
            + message [str]: 消息内容
        > 示例
        """

        try:
            send = lambda chain: self.adapter.send_message(target, chain)
            logger.info(message[:100])
            await send(message)
        except Exception as e:
            logger.error('无法发送消息: `%s`' % str(e))
            raise
