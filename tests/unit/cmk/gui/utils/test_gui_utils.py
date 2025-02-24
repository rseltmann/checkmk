#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.gui.default_name import unique_default_name_suggestion


@pytest.mark.parametrize(
    "template, used_names, suggestion",
    [
        (
            "stem",
            [],
            "stem_1",
        ),
        (
            "report",
            ["report_1", "all_hosts", "another_report"],
            "report_2",
        ),
    ],
)
def test_urlencode_vars(template: str, used_names: Sequence[str], suggestion: str) -> None:
    assert unique_default_name_suggestion(template, used_names) == suggestion
