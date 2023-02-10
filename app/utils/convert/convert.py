#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme
import base64
import math
from typing import AnyStr


# 将字节数转化为合适的大小单位
def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    if n < 1000:
        return f"{n}B"
    else:
        order = int(math.log2(n) / 10)
        human_readable = n / (1 << (order * 10))
        return f"{human_readable:.1f}{symbols[order - 1]}"


async def b64_encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string


async def b64_decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string


async def img2b64(img: AnyStr, path: bool = False) -> str:
    if path:
        with open(img, 'rb') as f:
            return 'base64://' + base64.b64encode(f.read()).decode()
    else:
        return 'base64://' + base64.b64encode(img).decode()
