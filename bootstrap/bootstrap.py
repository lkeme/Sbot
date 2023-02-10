#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import asyncio
import os
import sys
import time
import traceback
from threading import Thread

from rich.traceback import install as install_rich_traceback

from app.adapter.core import Core, set_bot
from app.config import config_mg
from app.logger import logger
from app.utils.singleton import Singleton
from .setting import version, app_name


class Bootstrap(Singleton):

    def __init__(self, plugins: list = None, binary: bool = False):
        super().__init__()
        self.core = Core()
        self.plugins = plugins
        self.binary = binary
        self.init(app_name, version)

    @staticmethod
    def change_console_title(title: str) -> None:
        """Windows 平台修改控制台标题"""
        import contextlib
        import ctypes
        with contextlib.suppress(Exception):
            ctypes.windll.kernel32.SetConsoleTitleW(title)

    def init(self, name, ver):
        # 捕获未处理的异常
        install_rich_traceback(console=None, show_locals=True)
        # 修改控制台窗口标题
        self.change_console_title(f'{name} {ver}')
        # 让PyCharm调试输出的信息换行
        if sys.gettrace() is not None:
            print('Debug Mode')

    def launch(self):
        try:
            set_bot(self.core)  # 将 bot 存储到 bot_store 中
            asyncio.run(
                self.core.register_plugins(self.plugins)
            )
            self.core.start_running()  # 启动钩子
            # self.core.loop()  # 开始监听事件循环
        except KeyboardInterrupt:
            # print('\n')
            logger.error(f'用户强制中断退出')
            sys.exit(0)
        except Exception as e:
            if config_mg.get('app', 'debug') == 'true':
                logger.error(f'出现全局错误: {e} 发生行数: {traceback.format_exc()}')
            else:
                logger.error(f'出现全局错误: {e}')
            time.sleep(60)
            sys.exit(0)

    def run_thread(self):
        if self.binary:
            # subp = subprocess.Popen("cd %s && .\go-cqhttp.exe -faststart" % go_cqhttp_path, shell=True,
            #                         stdout=subprocess.PIPE)
            # subp = subprocess.Popen("cd %s && ./go-cqhttp -faststart" % go_cqhttp_path, shell=True,
            #                         stdout=subprocess.PIPE)

            t1 = Thread(target=os.system, args=('cd cqhttp && ./go-cqhttp -faststart',))
            t1.start()
        else:
            pass
