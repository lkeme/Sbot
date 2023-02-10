#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import functools
import re
import warnings

import tzlocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.permission import UserLevel, USER, MESSAGE_CHECKER

warnings.filterwarnings("ignore")

scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
cron = CronTrigger


# @scheduler.scheduled_job("interval", name="清除缓存", minutes=30, misfire_grace_time=5)  # type: ignore

# functools
def re_filter(pattern: str, role: UserLevel = USER, enable: bool = False) -> callable:
    # I don't know how to add 2 decorators, it doesn't work well
    async def coro_null():
        return

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # 开关控制
            if not enable:
                return coro_null()

            event = args[0]
            if re.search(pattern, event.raw_message):
                # 消息权限
                if MESSAGE_CHECKER.is_msg_report(event) and not MESSAGE_CHECKER.permission_check(role, event):
                    return coro_null()
                # 通知权限
                # elif NOTICE_CHECKER.is_notice_report(event):
                #     if not NOTICE_CHECKER.permission_check(("user_id", role), event):
                #         return coro_null()  # return a null coroutine
                # 权限额外情况
                # else:
                #     print("权限额外情况")
                #     return coro_null()  # return a null coroutine

                return await func(*args, **kwargs)
            else:
                return await coro_null()  # return a null coroutine

        return wrapper

    return decorator
