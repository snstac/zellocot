#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Zello Cursor-On-Target Gateway.

"""
Zello Cursor-On-Target Gateway.
~~~~


:author: Greg Albrecht W2GMD <oss@undef.net>
:copyright: Copyright 2022 Greg Albrecht
:license: Apache License, Version 2.0
:source: <https://github.com/ampledata/zellocot>

"""

from .constants import (
    LOG_FORMAT,
    LOG_LEVEL,  # NOQA
    DEFAULT_POLL_INTERVAL,
    DEFAULT_COT_STALE,
)

from .functions import get_token, zello_to_cot, get_api_password, login  # NOQA

from .classes import ZelloWorker  # NOQA

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"
