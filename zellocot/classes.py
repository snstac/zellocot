#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ZelloCOT Class Definitions."""

import asyncio
import urllib

import aiohttp
import pytak

import zellocot


__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


class ZelloWorker(pytak.MessageWorker):

    """Reads Zello Locations, renders to COT, and puts on Queue."""

    def __init__(self, event_queue: asyncio.Queue, config):
        super().__init__(event_queue)
        self.cot_stale = config.get("COT_STALE")
        self.poll_interval: int = int(
            config.get("POLL_INTERVAL") or zellocot.DEFAULT_POLL_INTERVAL
        )

        self.url: urllib.parse.ParseResult = urllib.parse.urlparse(
            config.get("ZELLOWORK_URL")
        )
        self.api_key: str = config.get("API_KEY")
        self.password: str = config.get("PASSWORD")
        self.username: str = config.get("USERNAME")
        self.bbox_ne: str = config.get("BBOX_NE")
        self.bbox_sw: str = config.get("BBOX_SW")

    async def handle_message(self, locations: list) -> None:
        """
        Transforms Aircraft ADS-B data to COT and puts it onto tx queue.
        """
        if not isinstance(locations, list):
            self._logger.warning("Invalid locations data, should be a Python list.")
            return None

        if not locations:
            self._logger.warning("Empty locations list")
            return None

        _lac = len(locations)
        _acn = 1
        for loc in locations:
            event = zellocot.zello_to_cot(
                loc,
                stale=self.cot_stale,
            )

            if not event:
                self._logger.debug(f"Empty COT Event for loc={loc}")
                _acn += 1
                continue

            await self._put_event_queue(event)
            _acn += 1

    async def _get_zello_locations(self) -> None:
        url: str = f"{self.url.geturl()}/location/get?sid={self.sec_token.get('sid')}"
        params: dict = {
            "northeast[]": self.bbox_ne,
            "southwest[]": self.bbox_sw,
            "filter": "none",
        }
        async with aiohttp.ClientSession() as session:
            response = await session.request(method="GET", url=url, params=params)
            response = await response.json(content_type="text/html")
            assert response["code"] == "200"

            await self.handle_message(response["locations"])

    async def run(self) -> None:
        """Runs this Thread, Reads from Pollers."""
        self._logger.info("Running ZelloWorker with URL '%s'", self.url.geturl())

        self.sec_token = await zellocot.get_token(self.url)
        self.api_pass = zellocot.get_api_password(
            self.password, self.api_key, self.sec_token
        )
        if not await zellocot.login(
            self.url, self.username, self.api_pass, self.sec_token
        ):
            raise Exception("Login failure")

        while 1:
            await self._get_zello_locations()
            await asyncio.sleep(self.poll_interval)
