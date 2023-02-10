#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from dataclasses import dataclass

from .contact import Contact
from .group import Group
from ..role import Role


@dataclass
class Member(Contact):
    """
    > 说明
        群成员对象.
    > 参数
        + group [Group]: 群对象
        + user_id [int]: 用户 QQ 号
        + group_id [int]: 群号
        + nickname [str]: 群成员昵称
        + role [Role]: 群成员权限
        + last_sent_time [int]: 群成员最后发言时间戳
        + join_time [int]: 群成员加入群时间戳
    """
    group: Group
    user_id: int
    group_id: int
    nickname: str = None
    role: 'Role' = None
    last_sent_time: int = None
    join_time: int = None
