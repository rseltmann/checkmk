#!/usr/bin/env python3
# Copyright (C) 2022 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from kubernetes import client  # type: ignore[import]

from tests.unit.cmk.special_agents.agent_kubernetes.utils import FakeResponse

from cmk.special_agents.utils_kubernetes.schemata import api
from cmk.special_agents.utils_kubernetes.transform import parse_metadata_no_namespace


class TestAPINamespace:
    def test_parse_metadata(self, core_client: client.CoreV1Api, dummy_host: str) -> None:
        namespace_metadata = {
            "metadata": {
                "name": "checkmk-monitoring",
                "uid": "753292ba-5e0e-4267-a0f1-77a3c6b4d55e",
                "resourceVersion": "509",
                "creationTimestamp": "2022-03-25T13:24:42Z",
                "labels": {"kubernetes.io/metadata.name": "checkmk-monitoring"},
                "annotations": {
                    "kubectl.kubernetes.io/last-applied-configuration": '{"apiVersion":"v1","kind":"Namespace","metadata":{"annotations":{},"name":"checkmk-monitoring"}}\n'
                },
            },
        }

        namespace = core_client.api_client.deserialize(
            FakeResponse(namespace_metadata), "V1Namespace"
        )
        metadata = parse_metadata_no_namespace(namespace.metadata, api.NamespaceName)
        assert isinstance(metadata, api.MetaDataNoNamespace)
        assert metadata.name == "checkmk-monitoring"
        assert isinstance(metadata.creation_timestamp, float)
        assert metadata.labels == {
            "kubernetes.io/metadata.name": api.Label(
                name=api.LabelName("kubernetes.io/metadata.name"),
                value=api.LabelValue("checkmk-monitoring"),
            )
        }
        assert metadata.annotations == {}

    def test_parse_metadata_missing_annotations_and_labels(
        self, core_client: client.CoreV1Api, dummy_host: str
    ) -> None:
        namespace_metadata = {
            "metadata": {
                "name": "checkmk-monitoring",
                "uid": "753292ba-5e0e-4267-a0f1-77a3c6b4d55e",
                "resourceVersion": "509",
                "creationTimestamp": "2022-03-25T13:24:42Z",
            },
        }

        namespace = core_client.api_client.deserialize(
            FakeResponse(namespace_metadata), "V1Namespace"
        )
        metadata = parse_metadata_no_namespace(namespace.metadata, type_=api.NamespaceName)
        assert metadata.labels == {}
        assert metadata.annotations == {}
