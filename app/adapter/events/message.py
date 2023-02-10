#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme
from typing import Any

from app.adapter import Adapter
from app.adapter.actions import MessageAction
from app.adapter.contact import Friend, Group, Contact
from .event import Event

"""
消息上报判断
"""


class MessageEvent(Event):
    message_id: int
    message: str
    raw_message: str
    sender_name: str
    sender_role: str
    sender_self_id: int
    sub_type: str
    sender_id: int
    sender: Contact
    message_type: str
    time: int
    anonymous: object
    is_anonymous: bool = False
    temp_source: int
    group_id: int

    def __init__(self, adapter: Adapter, data: dict[str, Any]) -> None:
        super().__init__(adapter, "message", data)
        self.ma = MessageAction(self.adapter)

        self.separated(data)

        # if str(self.sender_id) in config_mg.get('general', 'admin_qq').split(','):
        #     self.fingerprint += ".admin"
        # if str(self.sender_id) == config_mg.get('general', 'master_qq'):
        #     self.fingerprint += ".master"

    def separated(self, data: dict[str, Any]) -> None:
        self.message_id = data['message_id']  # 消息的ID
        self.message = data['message']  # 消息链
        self.raw_message = data["raw_message"]  # 原始消息
        self.sender_name = data["sender"]["nickname"]  # 发送者昵称
        self.sender_self_id = data["self_id"]  # 机器人QQ号
        self.sub_type = data["sub_type"]  # 消息子类型
        self.message_type = data["message_type"]  # 消息类型
        self.time = data["time"]  # 消息时间戳
        self.sender_id = data["user_id"]  # 发送者QQ号
        if self.message_type == "group":
            self.temp_source = data["temp_source"]  # 临时会话来源
            self.sender_role = data["sender"]["role"]  # 发送者角色
            self.group_id = data["group_id"]  # 群
            self.sender = Group(group_id=self.group_id)  # 发送者群号
        else:
            self.sender = Friend(user_id=self.sender_id)

        if self.sub_type == "anonymous":
            self.anonymous = data["anonymous"]
            self.is_anonymous = True

    """
    > 说明
        快速对该消息对象进行回复.
    > 参数
        + message [MessageChain | Element | str]: 消息链或元素或纯文本 (纯文本会自动转为 ``Plain``, 元素会自动转化为 ``MessageChain``)
        + with_reply [bool]: 是否带上回复 ``Reply`` 当前消息链 [default=True]
    """

    async def reply(self, message: str, with_reply: bool = False) -> None:
        content = f"[CQ:reply,id={self.message_id}]{message}" if with_reply else message
        await self.ma.send_msg(self.sender, content)

    async def record(self, message: str) -> None:
        await self.ma.send_msg(self.sender, message)
