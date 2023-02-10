#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import time

from rich.console import Console


class Logger:
    def __init__(self, logger_name: str) -> None:
        self.logger_name = logger_name
        self.console = Console()
        self.formatter = '[white][%s][/white] [%s] %s'
        self._update_time()
        self.lambda_ = lambda msg, color: self._print(
            self.formatter % (self.time, self.logger_name, '[%s]%s[%s]' % (color, msg, color)))
        self.lambdas = {
            'info': lambda msg: self.lambda_(msg, 'white'),
            'success': lambda msg: self.lambda_(msg, 'bright_green'),
            'warning': lambda msg: self.lambda_(msg, 'bright_yellow'),
            'error': lambda msg: self.lambda_(msg, 'bright_red')
        }
        for k in self.lambdas:
            self.__setattr__(k, self.lambdas[k])

    def _update_time(self) -> None:
        self.time = time.strftime('%H:%M:%S', time.localtime())

    def _print(self, message: str) -> None:
        self._update_time()
        self.console.print(message)
