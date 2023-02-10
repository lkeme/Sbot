#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme


from app.adapter import Adapter
from .event import Event

"""
元上报判断
"""


class MetaEvent(Event):
    def __init__(self, adapter: Adapter, data: dict) -> None:
        super().__init__(adapter, "meta_event", data)

