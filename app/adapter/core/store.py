#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from app.logger import logger


class Store:
    def __init__(self):
        self.core: "Croe" = None


store = Store()


def set_bot(c: "Core") -> None:
    logger.info('设置机器人实例')
    store.core = c


def get_bot() -> "Core":
    logger.info('获取机器人实例')
    return store.core
