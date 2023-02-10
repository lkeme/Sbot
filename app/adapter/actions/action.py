#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from collections import defaultdict as ddict

from app.config import config_mg
from app.logger import logger
from app.request import request


async def get(terminal: str, params: dict = None) -> request.AsyncResponse:
    """
    add access_token to params
    and put infos to logger
    """
    params = ddict(lambda: None, params if params else {})
    url = config_mg.get('server', 'http_api') + terminal
    if not params['access_token']:
        params["access_token"] = config_mg.get('server', 'token')
    if not terminal.startswith('/'):
        logger.error("terminal must be like '/xxxx' !!!")

    resp = await request.get(url, params=params, stream=True, timeout=30)
    logger.debug(f"[GET] {terminal} {resp.status_code} {(await resp.text).strip()}")
    return resp
