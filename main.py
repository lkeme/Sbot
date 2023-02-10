#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from bootstrap import Bootstrap

if __name__ == '__main__':
    plugins = [
        # {'path': '路径(string)', 'remarks': '名称(string)'}, # 例子毋删
        {'path': 'base.default', 'remarks': '基础插件'},
        {'path': 'permission.default', 'remarks': '权限管理插件'},
        {'path': 'plugin.default', 'remarks': '插件管理器插件'},
        {'path': 'chatgpt.default', 'remarks': 'ChatGPT插件'},
        {'path': 'wf.default', 'remarks': 'WF插件'},
        {'path': 'qrcode.default', 'remarks': '二维码编解码'},
        {'path': 'weight.default', 'remarks': 'QQ权重查询'},
    ]
    bot = Bootstrap(plugins=plugins, binary=False)
    bot.launch()
