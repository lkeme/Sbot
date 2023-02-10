#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from enum import Enum


class Role(Enum):
    """
    > 说明
        群成员角色枚举类.
    """

    OWNER: str = 'owner'
    ADMIN: str = 'admin'
    MEMBER: str = 'member'
