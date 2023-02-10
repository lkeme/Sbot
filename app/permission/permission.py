#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from typing import NewType

UserLevel = NewType('UserLevel', int)

# 权限等级
ADMIN = UserLevel(100)
SU = UserLevel(90)
WHITE = UserLevel(80)
USER = UserLevel(70)
BLACK = UserLevel(-1)
