#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import time

import psutil

from app.utils.singleton import Singleton


class DashPanel(Singleton):
    """
    仪表盘
    """

    def __init__(self) -> None:
        super().__init__()
        self.start_time = time.time()

    @staticmethod
    async def memory_status() -> str:
        virtual_memory = psutil.virtual_memory()
        used_memory = virtual_memory.used / 1024 / 1024 / 1024
        free_memory = virtual_memory.free / 1024 / 1024 / 1024
        memory_percent = virtual_memory.percent
        # 内存使用：%0.2fG，使用率%0.1f%%，剩余内存：%0.2fG
        msg = "%0.2fG / %0.1f%% / %0.2fG" % (
            used_memory,
            memory_percent,
            free_memory,
        )
        return msg

    @staticmethod
    async def cpu_status() -> str:
        cpu_percent = psutil.cpu_percent(interval=1)
        # CPU使用率：%i%%
        msg = "%i%%" % cpu_percent
        return msg

    @staticmethod
    async def disk_status() -> str:
        content = ""
        for disk in psutil.disk_partitions():
            # 读写方式 光盘 or 有效磁盘类型
            if "cdrom" in disk.opts or disk.fstype == "":
                continue
            disk_name_arr = disk.device.split(":")
            disk_name = disk_name_arr[0]
            disk_info = psutil.disk_usage(disk.device)
            # 磁盘剩余空间，单位G
            free_disk_size = disk_info.free // 1024 // 1024 // 1024
            # 当前磁盘使用率和剩余空间G信息
            # "%s盘使用率：%s%%， 剩余空间：%iG
            info = "%s#%s%% %iG" % (
                disk_name,
                str(disk_info.percent),
                free_disk_size,
            )
            # print(info)
            # 拼接多个磁盘的信息
            content = content + info + "\n\t\t"
        msg = content[:-1].strip("\n\t\t")
        return msg

    async def bot_start_time(self) -> str:
        return time.strftime('%m-%d %H:%M:%S', time.localtime(self.start_time))

    async def bot_running_time(self) -> str:
        """
        获取运行时间
        """

        def format_nums(*time_num: int) -> list[str]:
            alist = []
            for num in time_num:
                alist.append(str(num) if num >= 10 else '0' + str(num))
            return alist

        worked_time = int(time.time() - self.start_time)
        day = worked_time // 3600 // 24
        hour = worked_time // 3600 % 24
        minute = worked_time // 60 % 60
        sec = worked_time % 60
        time_str_list = format_nums(day, hour, minute, sec)

        return ":".join(time_str_list)
