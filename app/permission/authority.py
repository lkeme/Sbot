#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import abc
from typing import Tuple, Union

from app.adapter.events import MessageEvent, RequestEvent, NoticeEvent, MetaEvent
from .permission import ADMIN, SU, WHITE, USER, BLACK, UserLevel
from ..logger import logger


class BaseAuthentication(abc.ABC):
    """
    权限校验器基类，所有权限校验器子类应该实现 check 方法
    """

    def __init__(self, permission_list: dict) -> None:
        self.auth_str_map = {
            ADMIN: 'admin',
            SU: 'superuser',
            WHITE: 'white',
            USER: 'user',
            BLACK: 'black'
        }
        self.admin: str = permission_list['admin']  # 管理员
        self.superuser: list = permission_list['superuser']  # 超级用户
        self.whitelist: list = permission_list['whitelist']  # 白名单
        self.blacklist: list = permission_list['blacklist']  # 黑名单
        self.valid_group: list = permission_list['valid_group']  # 有效群组

    # 元上报判断
    @staticmethod
    def is_meta_report(event: MetaEvent) -> bool: return event.post_type == 'meta_event'

    # 请求上报判断
    @staticmethod
    def is_req_report(event: RequestEvent) -> bool: return event.post_type == 'request'

    # 通知上报判断
    @staticmethod
    def is_notice_report(event: NoticeEvent) -> bool: return event.post_type == 'notice'

    # 消息上报判断
    @staticmethod
    def is_msg_report(event: MessageEvent) -> bool: return event.post_type == 'message'

    @classmethod
    @abc.abstractmethod
    def permission_check(cls, threshold_lvl: int, event: dict):
        pass


class MessageAuthentication(BaseAuthentication):
    """
    分级权限校验器，只适用于消息事件
    """

    def __init__(self, permission_list: dict) -> None:
        super().__init__(permission_list)

    def get_event_lvl(self, event: MessageEvent) -> UserLevel:
        """
        获得消息事件发起者的权限级别
        """
        # 黑名单身份判断 / 群聊匿名，直接等价黑名单 / 强制过滤系统信息
        if event.sender_id in self.blacklist or \
                event.is_anonymous or \
                event.sender_id in [1000000, 1000001, 80000000, 80000001, 0]:
            return BLACK
        # 优先判断是否为超管/绕过群组权限
        if event.sender_id == self.admin:
            return ADMIN
        # 其次判断是否为超级用户
        if event.sender_id in self.superuser:
            return SU
        # 最后判断是否为白名单
        if event.sender_id in self.whitelist:
            return WHITE
        # 默认为普通用户
        return USER

    def permission_check(self, expect_level: UserLevel, event: MessageEvent) -> bool:
        """
        消息事件权限检查
        """
        actual_level = self.get_event_lvl(event)

        logger.info(
            f"目标权限: {self.auth_str_map[expect_level]} |"
            f"当前权限: {self.auth_str_map[actual_level]} |"
            f"发送者: {event.sender_id} |"
            f"消息类型: {event.message_type}"
        )

        # 黑名单判断
        if actual_level == BLACK:
            return False
        # 管理员判断
        if actual_level == ADMIN:
            return True
        # 群组判断/如果不在有效群组内，直接返回False
        if event.message_type == "group":
            if event.group_id not in self.valid_group:
                return False
        else:
            # 临时会话 不处理
            if event.sub_type == "group":  # 不处理群临时会话
                return False
        # 等级检查
        return 0 < actual_level and actual_level >= expect_level


class NoticeAuthentication(BaseAuthentication):
    """
    通知事件权限校验器
    """

    def __init__(self, permission_list: dict) -> None:
        super().__init__(permission_list)

    def get_event_lvl(self, sender_id: Union[int, str]) -> UserLevel:
        """
        获得权限级别
        """
        # 黑名单身份判断
        if sender_id in self.blacklist:
            return BLACK
        # 直接身份判断
        if sender_id == self.admin:
            return ADMIN
        if sender_id in self.superuser:
            return SU
        if sender_id in self.whitelist:
            return WHITE
        else:
            return USER

    def permission_check(self, condition: Tuple[str, UserLevel], event: dict) -> bool:
        """
        检查通知事件的 id 类属性，在 UserLevel 级是否合法。
        """
        lvl = self.get_event_lvl(event[condition[0]])
        return 0 < lvl and lvl >= condition[1]


class MetaAuthentication(BaseAuthentication):

    def __init__(self, permission_list: dict) -> None:
        super().__init__(permission_list)

    def permission_check(self, threshold_lvl: UserLevel, event: dict) -> bool:
        """
        元事件上报权限检查
        """
        pass


class RequestAuthentication(BaseAuthentication):
    def __init__(self, permission_list: dict) -> None:
        super().__init__(permission_list)

    def permission_check(self, threshold_lvl: UserLevel, event: dict) -> bool:
        """
        请求上报权限检查
        """
        pass
