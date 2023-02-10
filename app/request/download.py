#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

import asyncio
import os
from threading import Thread
from typing import Coroutine, Optional

import aiofiles
import aiohttp

from app.logger import logger


class AsyncHttp:

    def __init__(self, download_path: str = "./download", chunk_size: int = 1024) -> None:
        self._loop = asyncio.new_event_loop()
        self._session = aiohttp.ClientSession(loop=self._loop)
        self._download_path = download_path
        self.chunk_size = chunk_size
        self.http = ""

        if not os.path.isdir(download_path):
            os.makedirs(download_path)

        self.__async_http_loop()

    async def _download_file(self, file_name: str, file_url: str) -> None:
        try:
            async with self._session.get(file_url) as req:
                if req.status != 200:
                    self.download_file_error(file_name, file_url, req.status)
                    return

                async with aiofiles.open("%s/%s" % (self._download_path, file_name), "wb") as file:
                    async for chunk in req.content.iter_chunked(self.chunk_size):
                        await file.write(chunk)

                    self.download_end(file_name, file_url, req.status)
        except Exception as err:
            self.download_file_run_error(err)

    async def _asynclink(self, api: str, data: dict = None) -> Optional[dict]:
        if data is None:
            data = {}

        json = await self.link("%s%s" % (self.http, api), mod="post", data=data)
        if json == {} or json is None:
            logger.warning("cqAPI 响应: None / {}")
            return None

        logger.debug("cqAPI 响应: %s" % json)

        if json["retcode"] != 0:
            self.api_link_error(json)

        return json

    async def link(self, url: str, mod: str = "get", data: dict = None, json: bool = True,
                   allow_redirects: bool = False, proxy: str = None, headers: dict = None, encoding: str = None) -> \
            Optional[dict]:
        if headers is None:
            headers = {}

        if data is None:
            data = {}

        if encoding is None:
            encoding = "utf-8"

        try:
            if mod == "get":
                async with self._session.get(url, data=data, allow_redirects=allow_redirects, proxy=proxy,
                                             headers=headers) as req:
                    if json:
                        http_data = await req.json(encoding=encoding)
                    else:
                        http_data = await req.text(encoding=encoding)

            if mod == "post":
                async with self._session.post(url, data=data, allow_redirects=allow_redirects, proxy=proxy,
                                              headers=headers) as req:
                    if json:
                        http_data = await req.json(encoding=encoding)
                    else:
                        http_data = await req.text(encoding=encoding)

            return http_data
        except Exception as err:
            self.api_link_run_error(err)

            return None

    def add_task(self, coroutine: Coroutine) -> None:
        asyncio.run_coroutine_threadsafe(coroutine, self._loop)

    def add(self, api: str, data: dict = None) -> None:
        if data is None:
            data = {}

        asyncio.run_coroutine_threadsafe(self._asynclink(api, data), self._loop)

    def download_path(self, download_path: str) -> None:
        if not os.path.isdir(download_path):
            os.makedirs(download_path)

        self._download_path = download_path

    def __async_http_loop(self) -> None:
        def task_loop_():
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()

        thread = Thread(target=task_loop_, name="asyncHttp_loop")
        thread.setDaemon(True)
        thread.start()

    async def _download_img(self, file: str) -> None:
        post_data = {
            "file": file
        }
        img_data = await self._asynclink("/get_image", data=post_data)
        if img_data is None:
            return None

        img_file = img_data["data"]
        await self._download_file(img_file["filename"], img_file["url"])

    def download_file(self, file_name: str, file_url: str) -> None:
        asyncio.run_coroutine_threadsafe(self._download_file(file_name, file_url), self._loop)

    def download_img(self, file: str) -> None:
        asyncio.run_coroutine_threadsafe(self._download_img(file), self._loop)

    def download_end(self, file_name: str, file_url: str, code: int) -> None:
        """
        下载完成
        """
        logger.info("%s 下载完成! code: %s" % (file_name, code))

    def download_file_error(self, file_name: str, file_url: str, code: int) -> None:
        """
        下载失败
        """
        logger.error("%s 下载失败... code: %s" % (file_name, code))

    def download_file_run_error(self, err: Exception) -> None:
        """
        下载时发生错误
        """
        logger.error("下载文件时发生错误 Error: %s" % err)
        logger.exception(err)

    def api_link_error(self, err_json: dict) -> None:
        """
        cqapi发生错误
        """
        logger.error("api 发生错误 %s: %s code: %s" % (err_json["msg"], err_json["wording"], err_json["retcode"]))

    def api_link_run_error(self, err: Exception) -> None:
        """
        cqapi请求时发生错误
        """
        logger.error("api 请求发生错误 Error: %s" % err)
        logger.exception(err)
