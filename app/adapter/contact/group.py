#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme


from dataclasses import dataclass

from .contact import Contact


@dataclass
class Group(Contact):
    """
    > 说明
        群对象.
    > 参数
        + group_id [int]: 群号
        + group_name [str]: 群昵称
        + max_member [int]: 群最大成员数
        + member_count [int]: 群当前成员数
        + group_level [int]: 群等级
        + group_create_time [int]: 群创建时间戳
    """
    group_id: int
    group_name: str = None
    max_member: int = None
    member_count: int = None
    group_level: int = None
    group_create_time: int = None
