#!/usr/bin/env python3
# Copyright (C) 2022 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from .dashlets import register_dashlets, StaticTextDashlet, StaticTextDashletConfig

__all__ = [
    "register_dashlets",
    "StaticTextDashletConfig",
    "StaticTextDashlet",
]
