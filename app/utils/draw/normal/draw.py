#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import base64
import io

from PIL import Image, ImageDraw, ImageFont

from ..base import get_current_path


async def image_draw(msg: str) -> str:
    # font_path = os.path.join(os.path.dirname(__file__), 'simhei.ttf')
    font_path = get_current_path('normal', 'simhei.ttf')
    ft_font = ImageFont.truetype(font_path, 16)
    width, height = ft_font.getsize_multiline(msg.strip())
    img = Image.new("RGB", (width + 20, height + 20), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), msg, fill=(0, 0, 0), font=ft_font)
    b_io = io.BytesIO()
    img.save(b_io, format="JPEG")
    base64_str = 'base64://' + base64.b64encode(b_io.getvalue()).decode()
    return base64_str
