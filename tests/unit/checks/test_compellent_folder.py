#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping, Sequence

import pytest

from tests.testlib import Check


@pytest.mark.parametrize(
    "info, expected_result", [([["", "", ""], ["2", "237273", "130456"]], [("2", {})])]
)
def test_inventory_dell_compellent_folder(
    info: Sequence[Sequence[str]], expected_result: Sequence[tuple[str, Mapping[object, object]]]
) -> None:
    result = Check("dell_compellent_folder").run_discovery(info)
    assert list(result) == expected_result
