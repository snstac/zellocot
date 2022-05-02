#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""ZelloCOT Functions."""

import datetime
import hashlib
import platform
import xml.etree.ElementTree as ET

import aiohttp

import pytak

import zellocot.constants


__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


async def get_token(url) -> dict:
    url: str = f"{url.geturl()}/user/gettoken"
    async with aiohttp.ClientSession() as session:
        response = await session.request(method="GET", url=url)
        response = await response.json(content_type="text/html")
        assert response["code"] == "200"
        return response


async def login(url, username, api_pass, sec_token: dict) -> bool:
    url = f"{url.geturl()}/user/login?sid={sec_token.get('sid')}"
    async with aiohttp.ClientSession() as session:
        response = await session.request(
            method="POST", url=url, data={"username": username, "password": api_pass}
        )
        response = await response.json(content_type="text/html")
        return response["code"] == "200"


def get_api_password(password, api_key, sec_token: dict) -> str:
    pass_hash = hashlib.md5()
    pass_hash.update(password.encode("utf8"))
    api_pass = hashlib.md5()
    api_pass.update(pass_hash.hexdigest().encode("utf8"))
    api_pass.update(sec_token.get("token").encode("utf8"))
    api_pass.update(api_key.encode("utf8"))
    return api_pass.hexdigest()


def zello_to_cot_xml(loc: dict, stale: int = None) -> ET.Element:
    """
    Transforms Zello Location to COT XML.
    """
    time = datetime.datetime.now(datetime.timezone.utc)
    cot_stale = stale or zellocot.constants.DEFAULT_COT_STALE

    cot_type: str = "a-f-G"
    name: str = loc["username"]
    callsign: str = loc["displayName"]

    point = ET.Element("point")
    point.set("lat", str(loc["latitude"]))
    point.set("lon", str(loc["longitude"]))

    point.set("ce", "9999999.0")
    point.set("le", "9999999.0")

    point.set("hae", str(loc.get("altitude", "9999999.0")))

    uid = ET.Element("UID")
    uid.set("Droid", name)

    contact = ET.Element("contact")
    contact.set("callsign", callsign)

    track = ET.Element("track")
    track.set("course", str(loc.get("heading", "9999999.0")))

    track.set("speed", str(loc.get("speed", "9999999.0")))

    detail = ET.Element("detail")
    detail.set("uid", name)
    detail.append(uid)
    detail.append(contact)
    detail.append(track)

    remarks = ET.Element("remarks")

    _remarks = (
        f"Zello User {name} ({callsign}) "
        f"Title: {loc['jobTitle']} "
        f"Battery: {loc['batteryLevel']} "
        f"Charging: {loc['chargingStatus']} "
        f"Signal: {loc['signalStrength']} "
        f"(via zellocot@{platform.node()})"
    )

    detail.set("remarks", _remarks)
    remarks.text = _remarks
    detail.append(remarks)

    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", cot_type)
    root.set("uid", f"ZELLO.{loc['username']}")
    root.set("how", "m-g")
    root.set("time", time.strftime(pytak.ISO_8601_UTC))
    root.set("start", time.strftime(pytak.ISO_8601_UTC))
    root.set(
        "stale",
        (time + datetime.timedelta(seconds=int(cot_stale))).strftime(
            pytak.ISO_8601_UTC
        ),
    )
    root.append(point)
    root.append(detail)

    return root


def zello_to_cot(loc: dict, stale: int = None) -> bytes:
    lat = loc.get("latitude")
    lon = loc.get("longitude")
    if lat is None or lon is None:
        return ""

    return ET.tostring(zello_to_cot_xml(loc, stale))
