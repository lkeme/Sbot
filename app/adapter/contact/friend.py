#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from dataclasses import dataclass

from .contact import Contact


@dataclass
class Friend(Contact):
    """
    > 说明
        好友对象.
    > 参数
        + user_id [int]: 好友 QQ 号
        + nickname [str]: 好友昵称
        + remark [str]: 备注名
    """
    user_id: int
    nickname: str = None
    remark: str = None
