#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from dataclasses import dataclass

from app.adapter import Adapter


@dataclass
class Data:
    pass


class Event:
    def __init__(self, adapter: Adapter, base_type: str, data: dict) -> None:
        self.post_type = base_type  # 上报类型
        self.adapter = adapter  # 适配器
        self.type = data[base_type + "_type"]  # 事件类型
        self.fingerprint = '.'.join([base_type, self.type])  # 指纹
        self.data = data  # 数据
