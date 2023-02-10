#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from .action import get


class GroupAction:
    def __init__(self, group_id: int) -> None:
        self.gid = group_id

    async def set_card(self, target: int, card: str):
        params = {
            "group_id": self.gid,
            "user_id": target,
            "card": card
        }
        await get('/set_group_card', params)

    async def mute(self, target: int, min: int = 30):
        params = {
            "group_id": self.gid,
            "user_id": target,
            "duration": min * 60
        }
        await get("/set_group_ban", params)
