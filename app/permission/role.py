#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from .permission import ADMIN, SU, WHITE, USER, BLACK


class Role:
    """
    角色类，包含不同权限角色的常量
    """

    def __init__(self) -> None:
        self.ADMIN = ADMIN
        self.SU = SU
        self.WHITE = WHITE
        self.BLACK = BLACK
        self.USER = USER

