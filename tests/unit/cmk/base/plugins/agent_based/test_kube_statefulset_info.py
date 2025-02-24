#!/usr/bin/env python3
# Copyright (C) 2021 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disallow_untyped_defs


import pytest

from cmk.base.plugins.agent_based.agent_based_api.v1 import Result, State
from cmk.base.plugins.agent_based.kube_statefulset_info import check_kube_statefulset_info
from cmk.base.plugins.agent_based.utils.kube import (
    NamespaceName,
    Selector,
    StatefulSetInfo,
    ThinContainers,
    Timestamp,
)


@pytest.mark.parametrize(
    "section, expected_check_result",
    [
        pytest.param(
            StatefulSetInfo(
                name="oh-lord",
                namespace=NamespaceName("have-mercy"),
                labels={},
                annotations={},
                selector=Selector(match_labels={}, match_expressions=[]),
                creation_timestamp=Timestamp(1600000000.0),
                containers=ThinContainers(images=frozenset({"i/name:0.5"}), names=["name"]),
                cluster="cluster",
                kubernetes_cluster_hostname="host",
            ),
            (
                Result(state=State.OK, summary="Name: oh-lord"),
                Result(state=State.OK, summary="Namespace: have-mercy"),
                Result(state=State.OK, summary="Age: 1 second"),
            ),
            id="overall look of StatefulSet with age 1 second",
        ),
    ],
)
def test_check_kube_statefulset_info(
    section: StatefulSetInfo, expected_check_result: tuple[Result, ...]
) -> None:
    assert tuple(check_kube_statefulset_info(1600000001.0, section)) == expected_check_result
