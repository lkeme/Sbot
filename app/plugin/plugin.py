#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from __future__ import annotations

import asyncio
from collections import defaultdict as ddict

from app.adapter.events import Event
from app.logger import logger


class PluginManager:
    def __init__(self):
        self.plugins = ddict(list)
        # 这里一般使用'指纹'来添加事件类型
        # 你也可以手动添加事件类型，比如'Onload'
        self.strip = lambda x: x[:x.rfind('.')]

    def split_fp(self, fp: str) -> list[str]:
        """
        turn 'a.b.c' -> ['a.b.c','a.b','a']
        """
        fps = []
        while fp:
            fps.append(fp)
            fp = self.strip(fp)
        return fps

    async def broadcast(self, event: Event):
        """
        fp : 'aaa.bbb.admin'
        fps: ['aaa.bbb.admin', 'aaa.bbb', 'aaa']
        """
        fps = self.split_fp(event.fingerprint)
        for fp in fps:
            if self.plugins[fp]:
                logger.debug(f"broadcast to: `{event.fingerprint}` plugins...")
                await asyncio.gather(*[
                    plugin(event) for plugin in self.plugins[fp]
                ])

    def reg_event(self, fingerprint: str) -> callable:
        def plugin(func):
            logger.debug(f'Registering {func} on {fingerprint}')
            self.plugins[fingerprint].append(func)

        return plugin
