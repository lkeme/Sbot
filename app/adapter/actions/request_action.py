#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from .action import get


class RequestAction:
    def __init__(self) -> None:
        pass

    @staticmethod
    async def pass_new_friend(flag: str):
        params = {
            "flag": flag
        }
        await get('/set_friend_add_request', params)

    @staticmethod
    async def pass_new_member(sub_type: str, flag: str):
        params = {
            "flag": flag,
            "sub_type": sub_type
        }
        await get("/set_group_add_request", params)

    @staticmethod
    async def revoke(msg_id: int):
        await get("/delete_msg", {"message_id": msg_id})
