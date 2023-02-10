#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from .event import Event
from .message import MessageEvent
from .meta import MetaEvent
from .notice import NoticeEvent
from .request import RequestEvent
from .unknown import UnknownEvent


class cqEvent:

    def __int__(self):
        """
        go-cqhttp 事件
        响应值查看: https://docs.go-cqhttp.org/event
        """
        self.__event = {
            # 好友私聊消息
            "message_private_friend": self.message_private_friend,
            # 群临时会话私聊消息
            "message_private_group": self.message_private_group,
            # 群中自身私聊消息
            "message_private_group_self": self.message_private_group_self,
            # 私聊消息
            "message_private_other": self.message_private_other,
            # 群消息
            "message_group_normal": self.message_group_normal,
            "message_group_anonymous": self.message_group_anonymous,
            # 自身群消息上报
            "message_sent_group_normal": self.message_sent_group_normal,
            # 自身消息私聊上报
            "message_sent_private_friend": self.message_sent_private_friend,
            # 群文件上传
            "notice_group_upload": self.notice_group_upload,
            # 群管理员变动
            "notice_group_admin_set": self.notice_group_admin_set,
            "notice_group_admin_unset": self.notice_group_admin_unset,
            # 群成员减少
            "notice_group_decrease_leave": self.notice_group_decrease_leave,
            "notice_group_decrease_kick": self.notice_group_decrease_kick,
            "notice_group_decrease_kick_me": self.notice_group_decrease_kick_me,
            # 群成员增加
            "notice_group_increase_approve": self.notice_group_increase_approve,
            "notice_group_increase_invite": self.notice_group_increase_invite,
            # 群禁言
            "notice_group_ban_ban": self.notice_group_ban_ban,
            "notice_group_ban_lift_ban": self.notice_group_ban_lift_ban,
            # 群消息撤回
            "notice_group_recall": self.notice_group_recall,
            # 群红包运气王提示
            "notice_notify_lucky_king": self.notice_notify_lucky_king,
            # 群成员荣誉变更提示
            "notice_notify_honor": self.notice_notify_honor,
            # 群成员名片更新
            "notice_group_card": self.notice_group_card,
            # 好友添加
            "notice_friend_add": self.notice_friend_add,
            # 好友消息撤回
            "notice_friend_recall": self.notice_friend_recall,
            # 好友/群内 戳一戳
            "notice_notify_poke": self.notice_notify_poke,
            # 接收到离线文件
            "notice_offline_file": self.notice_offline_file,
            # 其他客户端在线状态变更
            "notice_client_status": self.notice_client_status,
            # 精华消息添加
            "notice_essence_add": self.notice_essence_add,
            # 精华消息移出
            "notice_essence_delete": self.notice_essence_delete,
            # 加好友请求
            "request_friend": self.request_friend,
            # 加群请求
            "request_group_add": self.request_group_add,
            # 加群邀请
            "request_group_invite": self.request_group_invite,
            # 连接响应
            "meta_event_connect": self.meta_event_connect,
            # 心跳
            "meta_event": self.meta_event
        }

    def meta_event_connect(self, message):
        """
        连接响应
        """
        pass

    def meta_event(self, message):
        """
        心跳
        """
        pass

    def timing_start(self):
        """
        启动定时任务
        """
        pass

    def timing_jobs_start(self, job, run_count):
        """
        群列表定时任准备执行
        """
        pass

    def timing_job_end(self, job, run_count, group_id):
        """
        定时任务被执行
        """
        pass

    def timing_jobs_end(self, job, run_count):
        """
        群列表定时任务执行完成
        """
        pass

    def runTimingError(self, job, run_count, err, group_id):
        """
        定时任务执行错误
        """
        pass

    def on_group_msg(self, message):
        pass

    def on_private_msg(self, message):
        pass

    def at_bot(self, message, cqCode_list, cqCode):
        """
        接收到 at bot
        """
        pass

    def at(self, message, cqCode_list, cqCode):
        """
        接收到 at
        """
        pass

    def message_private_friend(self, message):
        """
        好友私聊消息
        """
        pass

    def message_private_group(self, message):
        """
        群临时会话私聊消息
        """
        pass

    def message_sent_private_friend(self, message):
        """
        自身消息私聊上报
        """
        pass

    def message_group_anonymous(self, message):
        """
        群匿名消息
        """
        pass

    def message_sent_group_normal(self, message):
        """
        群中自身消息上报
        """
        pass

    def message_private_group_self(self, message):
        """
        群中自身消息
        """
        pass

    def message_private_other(self, message):
        """
        私聊消息
        """
        pass

    def message_group_normal(self, message):
        """
        群消息
        """
        pass

    def notice_group_upload(self, message):
        """
        群文件上传
        """
        pass

    def notice_group_admin_set(self, message):
        """
        群管理员设置
        """
        pass

    def notice_group_admin_unset(self, message):
        """
        群管理员取消
        """
        pass

    def notice_group_decrease_leave(self, message):
        """
        群成员减少 - 主动退群
        """
        pass

    def notice_group_decrease_kick(self, message):
        """
        群成员减少 - 成员被踢
        """
        pass

    def notice_group_decrease_kick_me(self, message):
        """
        群成员减少 - 登录号被踢
        """
        pass

    def notice_group_increase_approve(self, message):
        """
        群成员增加 - 同意入群
        """
        pass

    def notice_group_increase_invite(self, message):
        """
        群成员增加 - 邀请入群
        """
        pass

    def notice_group_ban_ban(self, message):
        """
        群禁言
        """
        pass

    def notice_group_ban_lift_ban(self, message):
        """
        群解除禁言
        """
        pass

    def notice_group_recall(self, message):
        """
        群消息撤回
        """
        pass

    def notice_notify_lucky_king(self, message):
        """
        群红包运气王提示
        """
        pass

    def notice_notify_honor(self, message):
        """
        群成员荣誉变更提示
        honor_type 荣誉类型

        talkative:龙王
        performer:群聊之火
        emotion:快乐源泉
        """

        pass

    def notice_group_card(self, message):
        """
        群成员名片更新
        """
        pass

    def notice_friend_add(self, message):
        """
        好友添加
        """
        pass

    def notice_friend_recall(self, message):
        """
        好友消息撤回
        """
        pass

    def notice_notify_poke(self, message):
        """
        好友/群内 戳一戳
        """
        pass

    def notice_offline_file(self, message):
        """
        接收到离线文件
        """
        pass

    def notice_client_status(self, message):
        """
        其他客户端在线状态变更
        """
        pass

    def notice_essence_add(self, message):
        """
        精华消息添加
        """
        pass

    def notice_essence_delete(self, message):
        """
        精华消息移出
        """
        pass

    def request_friend(self, message):
        """
        加好友请求
        """
        pass

    def request_group_add(self, message):
        """
        加群请求
        """
        pass

    def request_group_invite(self, message):
        """
        加群邀请
        """
        pass
