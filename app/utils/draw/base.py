#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import os


def get_current_path(additional_path: str, resources: str) -> str:
    # print( __file__)
    # print(os.path.abspath(__file__))
    # print(os.path.dirname(os.path.realpath(__file__)))
    # print(os.path.split(os.path.realpath(__file__)))
    # print(os.path.abspath(os.path.dirname(__file__)))
    # return os.path.abspath(os.path.dirname(__file__))
    cp = os.path.dirname(os.path.realpath(__file__))
    return f"{cp}{os.sep}{additional_path}{os.sep}{resources}"
