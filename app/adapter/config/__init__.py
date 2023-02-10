#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme


from dataclasses import dataclass


class BaseAdapterConfig:
    """
    > 说明
        适配器配置基类.
    """

    ...


@dataclass
class AdapterConfig(BaseAdapterConfig):
    """
    > 说明
        CQHTTP 适配器配置类.
    > 参数
        + http_token [str]: 用于连接的 Access Token
        + http_host [str]: HTTP 主机地址 [default='127.0.0.1']
        + http_port [int]: HTTP 主机端口 [default=5700]
        + http_protocol [str]: HTTP 协议 [default='https://']
        + ws_host [str]: WebSocket 主机地址 [default='127.0.0.1']
        + ws_port [int]: WebSocket 主机端口 [default=6700]
        + ws_protocol [str]: WebSocket 协议 [default='ws://']
        + ws_reverse [bool]: 是否为反向 WebSocket [default=False]
    """
    http_token: str = '123456789'
    http_host: str = '127.0.0.1'
    http_port: int = 5700
    http_protocol: str = 'https://'
    ws_host: str = '0.0.0.0'
    ws_port: int = 5701
    ws_protocol: str = 'ws://'
    ws_reverse: bool = False
