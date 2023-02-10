#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from typing import Any

from .action import get


class SystemAction:
    def __init__(self) -> None:
        pass

    @staticmethod
    async def status() -> Any:
        resp = await get("/get_status")
        return await resp.json()
