#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

# from pathlib import Path
import os


def exits_path(path: str) -> bool:
    return os.path.exists(path)


def exits_file(path: str) -> bool:
    return os.path.isfile(path)


def create_path(path: str, mode=0o755):
    if not os.path.exists(path):
        os.makedirs(path, mode)
