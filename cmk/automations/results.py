#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from abc import ABC, abstractmethod
from ast import literal_eval
from dataclasses import astuple, dataclass
from typing import Any, Literal, Mapping, Optional, Tuple, Type, TypeVar

from cmk.utils.plugin_registry import Registry
from cmk.utils.python_printer import pformat
from cmk.utils.type_defs import (
    CheckPluginNameStr,
    ConfigurationWarnings,
    Gateways,
    NotifyAnalysisInfo,
    NotifyBulks,
    SerializedDiscoveryResponse,
    ServiceDetails,
    ServiceState,
)
from cmk.utils.type_defs import UpdateDNSCacheResult as UpdateDNSCacheResultRaw


class ResultTypeRegistry(Registry[Type["ABCAutomationResult"]]):
    def plugin_name(self, instance: Type["ABCAutomationResult"]) -> str:
        return instance.automation_call()


result_type_registry = ResultTypeRegistry()


class SerializedResult(str):
    ...


_DeserializedType = TypeVar("_DeserializedType", bound="ABCAutomationResult")


@dataclass  # type: ignore[misc]  # https://github.com/python/mypy/issues/5374
class ABCAutomationResult(ABC):
    def serialize(self) -> SerializedResult:
        return SerializedResult(pformat(astuple(self)))

    def to_pre_21(self) -> object:
        # Needed to support remote automation calls from an old central site to a new remote site.
        # In such cases, we must send the result in a format understood by the old central site.
        return astuple(self)[0]

    @classmethod
    def deserialize(
        cls: Type[_DeserializedType],
        serialized_result: SerializedResult,
    ) -> _DeserializedType:
        return cls(*literal_eval(serialized_result))

    @staticmethod
    @abstractmethod
    def automation_call() -> str:
        ...


@dataclass
class DiscoveryResult(ABCAutomationResult):
    serialized_response: SerializedDiscoveryResponse

    def to_pre_21(self) -> Mapping[Literal["results"], SerializedDiscoveryResponse]:
        return {"results": self.serialized_response}

    @staticmethod
    def automation_call() -> str:
        return "inventory"


result_type_registry.register(DiscoveryResult)


@dataclass
class TryDiscoveryResult(ABCAutomationResult):
    result: Mapping[str, Any]

    @staticmethod
    def automation_call() -> str:
        return "try-inventory"


result_type_registry.register(TryDiscoveryResult)


@dataclass
class SetAutochecksResult(ABCAutomationResult):
    _result: None

    @staticmethod
    def automation_call() -> str:
        return "set-autochecks"


result_type_registry.register(SetAutochecksResult)


@dataclass
class UpdateHostLabelsResult(ABCAutomationResult):
    _result: None

    @staticmethod
    def automation_call() -> str:
        return "update-host-labels"


result_type_registry.register(UpdateHostLabelsResult)


@dataclass
class RenameHostsResult(ABCAutomationResult):
    action_counts: Mapping[str, int]

    @staticmethod
    def automation_call() -> str:
        return "rename-hosts"


result_type_registry.register(RenameHostsResult)


@dataclass
class AnalyseServiceResult(ABCAutomationResult):
    service_info: Mapping

    @staticmethod
    def automation_call() -> str:
        return "analyse-service"


result_type_registry.register(AnalyseServiceResult)


@dataclass
class AnalyseHostResult(ABCAutomationResult):
    label_info: Mapping

    @staticmethod
    def automation_call() -> str:
        return "analyse-host"


result_type_registry.register(AnalyseHostResult)


@dataclass
class DeleteHostsResult(ABCAutomationResult):
    _result: None

    @staticmethod
    def automation_call() -> str:
        return "delete-hosts"


result_type_registry.register(DeleteHostsResult)


@dataclass
class DeleteHostsKnownRemoteResult(ABCAutomationResult):
    _result: None

    @staticmethod
    def automation_call() -> str:
        return "delete-hosts-known-remote"


result_type_registry.register(DeleteHostsKnownRemoteResult)


@dataclass
class RestartResult(ABCAutomationResult):
    config_warnings: ConfigurationWarnings

    @staticmethod
    def automation_call() -> str:
        return "restart"


result_type_registry.register(RestartResult)


@dataclass
class ReloadResult(RestartResult):
    @staticmethod
    def automation_call() -> str:
        return "reload"


result_type_registry.register(ReloadResult)


@dataclass
class GetConfigurationResult(ABCAutomationResult):
    result: Mapping[str, Any]

    @staticmethod
    def automation_call() -> str:
        return "get-configuration"


result_type_registry.register(GetConfigurationResult)


@dataclass
class GetCheckInformationResult(ABCAutomationResult):
    plugin_infos: Mapping[CheckPluginNameStr, Mapping[str, Any]]

    @staticmethod
    def automation_call() -> str:
        return "get-check-information"


result_type_registry.register(GetCheckInformationResult)


@dataclass
class GetSectionInformationResult(ABCAutomationResult):
    section_infos: Mapping[str, Mapping[str, str]]

    @staticmethod
    def automation_call() -> str:
        return "get-section-information"


result_type_registry.register(GetSectionInformationResult)


@dataclass
class ScanParentsResult(ABCAutomationResult):
    gateways: Gateways

    @staticmethod
    def automation_call() -> str:
        return "scan-parents"


result_type_registry.register(ScanParentsResult)


@dataclass
class DiagHostResult(ABCAutomationResult):
    result: Tuple[int, str]

    @staticmethod
    def automation_call() -> str:
        return "diag-host"


result_type_registry.register(DiagHostResult)


@dataclass
class ActiveCheckResult(ABCAutomationResult):
    result: Optional[Tuple[ServiceState, ServiceDetails]]

    @staticmethod
    def automation_call() -> str:
        return "active-check"


result_type_registry.register(ActiveCheckResult)


@dataclass
class UpdateDNSCacheResult(ABCAutomationResult):
    result: UpdateDNSCacheResultRaw

    @staticmethod
    def automation_call() -> str:
        return "update-dns-cache"


result_type_registry.register(UpdateDNSCacheResult)


@dataclass
class GetAgentOutputResult(ABCAutomationResult):
    result: Tuple[bool, ServiceDetails, bytes]

    @staticmethod
    def automation_call() -> str:
        return "get-agent-output"


result_type_registry.register(GetAgentOutputResult)


@dataclass
class NotificationReplayResult(ABCAutomationResult):
    _result: None

    @staticmethod
    def automation_call() -> str:
        return "notification-replay"


result_type_registry.register(NotificationReplayResult)


@dataclass
class NotificationAnalyseResult(ABCAutomationResult):
    result: Optional[NotifyAnalysisInfo]

    @staticmethod
    def automation_call() -> str:
        return "notification-analyse"


result_type_registry.register(NotificationAnalyseResult)


@dataclass
class NotificationGetBulksResult(ABCAutomationResult):
    result: NotifyBulks

    @staticmethod
    def automation_call() -> str:
        return "notification-get-bulks"


result_type_registry.register(NotificationGetBulksResult)


@dataclass
class GetServiceConfigurationsResult(ABCAutomationResult):
    result: Mapping

    @staticmethod
    def automation_call() -> str:
        return "get-service-configurations"


result_type_registry.register(GetServiceConfigurationsResult)


@dataclass
class GetLabelsOfResult(ABCAutomationResult):
    result: Mapping[str, Any]

    @staticmethod
    def automation_call() -> str:
        return "get-labels-of"


result_type_registry.register(GetLabelsOfResult)


@dataclass
class CreateDiagnosticsDumpResult(ABCAutomationResult):
    result: Mapping[str, Any]

    @staticmethod
    def automation_call() -> str:
        return "create-diagnostics-dump"


result_type_registry.register(CreateDiagnosticsDumpResult)


@dataclass
class BakeAgentsResult(ABCAutomationResult):
    warnings: Optional[str]

    @staticmethod
    def automation_call() -> str:
        return "bake-agents"


result_type_registry.register(BakeAgentsResult)
