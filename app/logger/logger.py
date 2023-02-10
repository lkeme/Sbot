#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import logging.handlers

import colorlog
from rich.console import Console

from app.config import config_mg

log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

logger = logging.getLogger('Logger')
logger.console = Console()

# 输出到控制台
ch = logging.StreamHandler()
# 输出到文件
# 设置回滚日志句柄
# fh = logging.FileHandler(  # 一般用这个
fh = logging.handlers.RotatingFileHandler(
    filename=config_mg.get('log', 'log_file_name'),
    mode='a',
    encoding='utf8',
    maxBytes=config_mg.get_int('log', 'max_bytes'),
    backupCount=config_mg.get_int('log', 'backup_count')
)

# logging.INFO
fh.setLevel(config_mg.get_int('log', 'file_log_level'))
# logging.DEBUG
ch.setLevel(config_mg.get_int('log', 'console_log_level'))

# 日志输出格式
file_formatter = logging.Formatter(
    fmt='[%(asctime)s.%(msecs)03d %(filename)s] [%(levelname)s] : %(message)s',
    datefmt='%Y-%m-%d  %H:%M:%S'
)
console_formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s[%(asctime)s.%(msecs)03d %(filename)s] [%(levelname)s] : %(message)s',
    # fmt='\033[0m[%(asctime)s][%(threadName)s/%(levelname)s] PyCqBot: %(message)s\033[0m',
    datefmt='%Y-%m-%d  %H:%M:%S',
    log_colors=log_colors_config
)
ch.setFormatter(console_formatter)
fh.setFormatter(file_formatter)

# 重复日志问题：
# 1、防止多次addHandler；
# 2、loggername 保证每次添加的时候不一样；
# 3、显示完log之后调用removeHandler

if not logger.handlers:
    logger.addHandler(ch)
    logger.addHandler(fh)

ch.close()
fh.close()
