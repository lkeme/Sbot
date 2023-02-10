#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from app.adapter import Adapter
from .event import Event

"""
请求上报判断
"""

class RequestEvent(Event):
    def __init__(self, adapter: Adapter, data: dict) -> None:
        super().__init__(adapter, "request", data)

    async def info_new_friend(self) -> tuple:
        return self.data['user_id'], self.data['comment'], self.data['flag']

    async def info_new_member(self):
        pass
