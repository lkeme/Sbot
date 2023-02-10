#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme
from typing import Any

from app.adapter import Adapter
from .event import Event

"""
通知上报判断
"""


class NoticeEvent(Event):
    time: int  # 通知时间戳
    self_id: int  # 机器人QQ号
    notice_type: str  # 通知类型
    sub_type: str  # 通知子类型

    def __init__(self, adapter: Adapter, data: dict) -> None:
        super().__init__(adapter, "notice", data)

    def separated(self, data: dict[str, Any]) -> None:
        """
       判断事件是否为通知，可以用的类型有：
           group_upload(群文件上传)  group_admin(群管理员变更)  group_decrease(群成员减少)  group_increase(群成员增加)
           group_ban(群成员禁言)  friend_add(好友添加)  group_recall(群消息撤回)  friend_recall(好友消息撤回)
           group_card(群名片变更)  offline_file(离线文件上传)  client_status(客户端状态变更)  essence(精华消息)
           notify(系统通知)
       Args:
           notice_type: 可选，指定 notice_type 内容是否一致，作为附加条件进行判断
       """
        self.notice_type = data["notice_type"]  # 通知类型
        self.sub_type = data["sub_type"]  # 通知子类型

    async def get_id(self) -> tuple:
        try:
            return self.data["group_id"], self.data['user_id']
        except Exception as e:  # noqa
            return 0, 0
