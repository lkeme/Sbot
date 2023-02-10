#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from app.adapter import Adapter
from .event import Event


class UnknownEvent(Event):
    def __init__(self, adapter: Adapter, data: dict) -> None:
        super().__init__(adapter, "unknown", data)
