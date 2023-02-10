#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from app.config import config_mg
from .authority import MetaAuthentication, NoticeAuthentication, MessageAuthentication, RequestAuthentication
from .permission import ADMIN, SU, WHITE, USER, BLACK, UserLevel
from .role import Role

ROLE = Role()

MESSAGE_CHECKER = None
NOTICE_CHECKER = None
REQUEST_CHECKER = None
META_CHECKER = None


def load_permission() -> None:
    """加载权限"""
    global ROLE, MESSAGE_CHECKER, NOTICE_CHECKER, REQUEST_CHECKER, META_CHECKER

    permission_list = {
        'admin': config_mg.get_int('permission', 'admin', appoint='plugin'),
        'superuser': config_mg.get_list('permission', 'superuser', appoint='plugin'),
        'whitelist': config_mg.get_list('permission', 'blacklist', appoint='plugin'),
        'blacklist': config_mg.get_list('permission', 'blacklist', appoint='plugin'),
        'valid_group': config_mg.get_list('permission', 'valid_group', appoint='plugin')
    }

    MESSAGE_CHECKER = MessageAuthentication(permission_list)
    NOTICE_CHECKER = NoticeAuthentication(permission_list)
    REQUEST_CHECKER = RequestAuthentication(permission_list)
    META_CHECKER = MetaAuthentication(permission_list)


load_permission()
