#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import ast
import asyncio
import os
import threading
from typing import TypeVar, Any, Union, Iterable, Coroutine

from app.utils.configupdater import ConfigUpdater, Section
from app.utils.path import exits_file

lock = threading.Lock()

T = TypeVar("T", bound="ConfigManager")


class ConfigManager:
    """
    ConfigManager 配置管理器
    https://github.com/pyscaffold/configupdater
    """

    dependency: list[Coroutine] = []  # 依赖重启

    config: ConfigUpdater = None  # 当前配置文件

    def __init__(self: T) -> None:
        self.suffix: str = '.ini'  # 配置文件后缀
        self.config_list: dict[str:ConfigUpdater] = {
            'app_config': None,
            'plugin_config': None,
        }  # 配置文件列表
        self.root: str = f"{os.getcwd()}{os.sep}%s{self.suffix}"  # 配置文件匹配路径
        self.load()  # 加载配置文件

    def load(self: T) -> None:
        """
        加载配置文件
        """
        # if ((os.path.splitext(file_name)[1]).lower() == '.ini')
        #     and os.path.isfile(f'{self.root}/{file_name}'):
        # file_names = os.listdir(self.root)  # 获取文件夹下的所有文件和文件夹名称

        for prefix in self.config_list:
            path = self.root % prefix
            if not exits_file(path):
                raise FileNotFoundError(f"配置文件不存在: {path}")
            # 加载配置文件
            self.config_list[prefix] = ConfigUpdater()
            self.config_list[prefix].read(filename=path, encoding='utf-8')

    def add_coroutine(self, coroutine: Union[Coroutine, Any]) -> None:
        """
        异步执行
        """
        self.dependency.append(coroutine)

    @staticmethod
    def coroutine(coroutine: Union[Coroutine, Any]) -> Any:
        """
        异步执行
        """
        return asyncio.run(coroutine)

    def reload(self: T) -> None:
        """
        重新加载配置文件
        """
        self.load()
        for d in self.dependency:
            self.coroutine(d)

    def appoint(self: T, appoint: str = 'app') -> str:
        """
        指定配置文件
        """
        f = f'{appoint}_config'
        if f not in self.config_list:
            raise KeyError(f"配置文件不存在: {appoint}")
        return f

    def get(self: T, section: str, option: str, default: str = '', appoint: str = 'app') -> str:
        """
        获取配置文件的值
        """
        if not self.config_list[self.appoint(appoint)].has_option(section, option):
            return default
        return self.config_list[self.appoint(appoint)].get(section, option).value

    def set(self: T, section: str, option: str, value: Union[list, None, str, Iterable[str]] = '',
            appoint: str = 'app') -> None:
        """
        设置配置文件的值
        """
        if isinstance(value, list):
            value = str(value)
        self.config_list[self.appoint(appoint)].set(section, option, value)

    def get_bool(self: T, section: str, option: str, default: bool = False, appoint: str = 'app') -> bool:
        """
        获取配置文件的布尔值
        """
        try:
            if not self.config_list[self.appoint(appoint)].has_option(section, option):
                return default
            return self.get(section, option, '', appoint).lower() in ('true', '1', 'yes', 'y')
        except (ValueError, Exception):
            return default

    def get_int(self: T, section: str, option: str, default: int = 0, appoint: str = 'app') -> int:
        """
        获取配置文件的整数值
        """
        try:
            if not self.config_list[self.appoint(appoint)].has_option(section, option):
                return default
            return int(self.get(section, option, '', appoint))
        except (ValueError, Exception) as e:
            return default

    def get_float(self: T, section: str, option: str, default: float = 0.0, appoint: str = 'app') -> float:
        """
        获取配置文件的浮点值
        """
        try:
            if not self.config_list[self.appoint(appoint)].has_option(section, option):
                return default
            return float(self.get(section, option, '', appoint))
        except (ValueError, Exception) as e:
            return default

    def get_list(self: T, section: str, option: str, default: list = None, appoint: str = 'app') -> list:
        """
        获取配置文件的列表值
        """
        try:
            if not self.config_list[self.appoint(appoint)].has_option(section, option):
                return default
            return ast.literal_eval(self.get(section, option, '', appoint))
        except (ValueError, Exception):
            return default

    def add(self: T, section: str, option: str, value: Union[list, None, str, Iterable[str]] = '',
            appoint: str = 'app') -> None:
        """
        添加配置文件的值
        """
        if isinstance(value, list):
            value = str(value)

        old_value = self.get(section, option, '', appoint)
        value = old_value or value
        try:
            self.config_list[self.appoint(appoint)][section][option] = value
        except Exception as e:  # noqa
            self.config_list[self.appoint(appoint)].add_section(Section(name=section, raw_comment=f' # {section}配置'))
            self.config_list[self.appoint(appoint)][section][option] = value

    def save(self: T, file_name: Union[str, Any] = None, appoint: str = 'app') -> None:
        """
        保存配置文件
        """
        try:
            if file_name is None:
                self.config_list[self.appoint(appoint)].update_file()
            else:
                self.config_list[self.appoint(appoint)].write(open(file_name, 'w', encoding='utf-8'))
        except (IOError, Exception):
            raise IOError(f"配置文件保存失败: {file_name}")

        self.reload()
