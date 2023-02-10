#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

class Singleton:
    """
    单例类
    """
    __judge = None  # 单例类

    def __new__(cls, *args, **kwargs):
        if cls.__judge is None or cls.__judge.__path is None:
            cls.__judge = object.__new__(cls)
        return cls.__judge
