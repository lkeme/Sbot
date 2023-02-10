#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme


class BotException(Exception):
    """
    bot 异常基类
    """

    def __init__(self, err: str):
        super().__init__(self)
        self.err = f'[{self.__class__.__name__}] {err}'
        self.origin_err = err

    def __str__(self):
        return self.err


class BotUnSupportCmdFlag(BotException):
    def __init__(self, err: str):
        super().__init__(err)


class BotUnknownEvent(BotException):
    def __init__(self, err: str):
        super().__init__(err)


class BotUnexpectedEvent(BotException):
    def __init__(self, err: str):
        super().__init__(err)


class BotCmdWrongParams(BotException):
    def __init__(self, err: str):
        super().__init__(err)


class BotUnknownCmdName(BotException):
    def __init__(self, err: str):
        super().__init__(err)
