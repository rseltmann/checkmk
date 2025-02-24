#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

"""
Tests for legacy tuple rulesets.
"""


# pylint: disable=redefined-outer-name

import pytest

from tests.testlib.base import Scenario

import cmk.utils.rulesets.tuple_rulesets as tuple_rulesets
import cmk.utils.version as cmk_version

import cmk.base.config as config
from cmk.base.config import Ruleset


@pytest.fixture(autouse=True)
def fake_version(monkeypatch):
    monkeypatch.setattr(cmk_version, "omd_version", lambda: "1.4.0i1.cee")


@pytest.fixture()
def ts(monkeypatch):
    ts = Scenario(site_id="site1")
    ts.add_host("host1", tags={"agent": "no-agent", "criticality": "test"})
    ts.add_host("host2", tags={"agent": "no-agent"})
    ts.add_host("host3", tags={"agent": "no-agent", "site": "site2"})
    ts.apply(monkeypatch)
    return ts


def test_service_extra_conf(ts: Scenario) -> None:
    ruleset: Ruleset[str] = [
        {"condition": {}, "options": {}, "value": "1"},
        {"condition": {}, "options": {}, "value": "2"},
        {"condition": {"host_tags": {"agent": "no-agent"}}, "options": {}, "value": "3"},
        {"condition": {"host_tags": {"criticality": "test"}}, "options": {}, "value": "4"},
        {"condition": {"host_tags": {"tag3": "tag3"}}, "options": {}, "value": "5"},
        {
            "condition": {"host_tags": {"tag3": "tag3"}, "host_name": ["host1"]},
            "options": {},
            "value": "6",
        },
        {"condition": {"host_name": ["host1"]}, "options": {}, "value": "7"},
        {
            "condition": {"service_description": [{"$regex": "service1$"}], "host_name": ["host1"]},
            "options": {},
            "value": "8",
        },
        {
            "condition": {"service_description": [{"$regex": "ser$"}], "host_name": ["host1"]},
            "options": {},
            "value": "9",
        },
        {
            "condition": {"service_description": [{"$regex": "^serv$"}], "host_name": ["host1"]},
            "options": {},
            "value": "10",
        },
        {"condition": {"host_name": [{"$regex": "host"}]}, "options": {}, "value": "11"},
        {"condition": {"host_name": {"$nor": ["host2"]}}, "options": {}, "value": "12"},
    ]

    assert ts.config_cache.service_extra_conf("host1", "service1", ruleset) == [
        "1",
        "2",
        "3",
        "4",
        "7",
        "8",
        "11",
        "12",
    ]

    assert ts.config_cache.service_extra_conf("host1", "serv", ruleset) == [
        "1",
        "2",
        "3",
        "4",
        "7",
        "10",
        "11",
        "12",
    ]

    assert ts.config_cache.service_extra_conf("host2", "service1", ruleset) == ["1", "2", "3", "11"]


@pytest.fixture(scope="function")
def host_ruleset():
    return [
        {"condition": {}, "options": {}, "value": {"1": True}},
        {"condition": {"host_tags": {"agent": "no-agent"}}, "options": {}, "value": {"2": True}},
        {"condition": {"host_tags": {"criticality": "test"}}, "options": {}, "value": {"3": True}},
        {"condition": {"host_tags": {"tag3": "tag3"}}, "options": {}, "value": {"4": True}},
        {
            "condition": {"host_tags": {"agent": "no-agent"}, "host_name": ["host1"]},
            "options": {},
            "value": {"5": True},
        },
        {
            "condition": {"host_tags": {"tag3": "tag3"}, "host_name": ["host1"]},
            "options": {},
            "value": {"6": True},
        },
        {"condition": {"host_name": ["host1"]}, "options": {}, "value": {"7": True}},
        {"condition": {"host_name": [{"$regex": "host"}]}, "options": {}, "value": {"8": True}},
        {"condition": {"host_name": {"$nor": ["host2"]}}, "options": {}, "value": {"9": True}},
    ]


def test_host_extra_conf(ts: Scenario, host_ruleset: Ruleset[object]) -> None:
    assert ts.config_cache.host_extra_conf("host1", host_ruleset) == [
        {"1": True},
        {"2": True},
        {"3": True},
        {"5": True},
        {"7": True},
        {"8": True},
        {"9": True},
    ]

    assert ts.config_cache.host_extra_conf("host2", host_ruleset) == [
        {"1": True},
        {"2": True},
        {"8": True},
    ]


def test_host_extra_conf_merged(ts: Scenario, host_ruleset: Ruleset[object]) -> None:
    assert ts.config_cache.host_extra_conf_merged("host1", host_ruleset) == {
        "1": True,
        "2": True,
        "3": True,
        "5": True,
        "7": True,
        "8": True,
        "9": True,
    }

    assert ts.config_cache.host_extra_conf_merged("host2", host_ruleset) == {
        "1": True,
        "2": True,
        "8": True,
    }


@pytest.mark.parametrize(
    "parameters",
    [
        # ruleset, outcome host1, outcome host2
        ([], False, False),
        (
            [{"condition": {}, "options": {}, "value": False}],
            False,
            False,
        ),
        ([{"condition": {}, "options": {}, "value": True}], True, True),
        (
            [{"condition": {"host_name": {"$nor": ["host1"]}}, "options": {}, "value": True}],
            False,
            True,
        ),
        (
            [
                {
                    "condition": {"host_name": {"$nor": ["host1", "host2"]}},
                    "options": {},
                    "value": True,
                }
            ],
            False,
            False,
        ),
        (
            [{"condition": {"host_tags": {"criticality": "test"}}, "options": {}, "value": True}],
            True,
            False,
        ),
        (
            [
                {
                    "condition": {
                        "host_tags": {"criticality": "test"},
                        "host_name": {"$nor": ["host1"]},
                    },
                    "options": {},
                    "value": True,
                }
            ],
            False,
            False,
        ),
        (
            [{"condition": {"host_name": {"$nor": ["host1"]}}, "options": {}, "value": True}],
            False,
            True,
        ),
        (
            [{"condition": {"host_name": {"$nor": ["host1"]}}, "options": {}, "value": False}],
            False,
            False,
        ),
        (
            [
                {
                    "condition": {
                        "host_tags": {"criticality": "test"},
                        "host_name": {"$nor": ["host1"]},
                    },
                    "options": {},
                    "value": False,
                }
            ],
            False,
            False,
        ),
        (
            [
                {
                    "condition": {"service_description": [{"$regex": "serv"}]},
                    "options": {},
                    "value": True,
                }
            ],
            True,
            True,
        ),
        (
            [
                {
                    "condition": {"service_description": [{"$regex": "serv"}]},
                    "options": {},
                    "value": False,
                }
            ],
            False,
            False,
        ),
        (
            [
                {
                    "condition": {"service_description": [{"$regex": "service1"}]},
                    "options": {},
                    "value": False,
                }
            ],
            False,
            False,
        ),
        # Dual rule test, first rule matches host1 - negates -> False
        #                 second rule matches host2 -> True
        (
            [
                {
                    "condition": {"service_description": [{"$regex": "service1"}]},
                    "options": {},
                    "value": False,
                },
                {"condition": {}, "options": {}, "value": True},
            ],
            False,
            True,
        ),
    ],
)
def test_in_boolean_serviceconf_list(ts: Scenario, parameters: tuple[Ruleset, bool, bool]) -> None:
    ruleset, outcome_host1, outcome_host2 = parameters

    assert (
        ts.config_cache.in_boolean_serviceconf_list("host1", "service1", ruleset) == outcome_host1
    )
    assert (
        ts.config_cache.in_boolean_serviceconf_list("host2", "service2", ruleset) == outcome_host2
    )


def test_all_matching_hosts(ts: Scenario) -> None:
    config_cache = ts.config_cache
    assert config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
        {"host_tags": {"agent": "no-agent"}}, with_foreign_hosts=False
    ) == {"host1", "host2"}

    assert config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
        {"host_tags": {"criticality": "test"}}, with_foreign_hosts=False
    ) == {"host1"}

    assert config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
        {"host_tags": {"criticality": {"$ne": "test"}}}, with_foreign_hosts=False
    ) == {"host2"}

    assert config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
        {"host_tags": {"criticality": {"$ne": "test"}}}, with_foreign_hosts=True
    ) == {"host2", "host3"}

    assert (
        config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
            {"host_tags": {"agent": "no-agent"}, "host_name": []}, with_foreign_hosts=True
        )
        == set()
    )

    assert config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
        {"host_tags": {"agent": "no-agent"}, "host_name": ["host1"]}, with_foreign_hosts=True
    ) == {"host1"}

    assert (
        config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
            {"host_tags": {"agent": {"$ne": "no-agent"}}, "host_name": ["host1"]},
            with_foreign_hosts=False,
        )
        == set()
    )

    assert config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
        {"host_tags": {"agent": "no-agent"}, "host_name": [{"$regex": "h"}]},
        with_foreign_hosts=False,
    ) == {"host1", "host2"}

    assert config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
        {"host_tags": {"agent": "no-agent"}, "host_name": [{"$regex": ".*2"}]},
        with_foreign_hosts=False,
    ) == {"host2"}

    assert config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
        {"host_tags": {"agent": "no-agent"}, "host_name": [{"$regex": ".*2$"}]},
        with_foreign_hosts=False,
    ) == {"host2"}

    assert (
        config_cache.ruleset_matcher.ruleset_optimizer._all_matching_hosts(
            {"host_tags": {"agent": "no-agent"}, "host_name": [{"$regex": "2"}]},
            with_foreign_hosts=False,
        )
        == set()
    )


def test_in_extraconf_hostlist() -> None:
    assert tuple_rulesets.in_extraconf_hostlist(tuple_rulesets.ALL_HOSTS, "host1") is True
    assert tuple_rulesets.in_extraconf_hostlist([], "host1") is False

    assert tuple_rulesets.in_extraconf_hostlist(["host2", "host1"], "host1") is True
    assert tuple_rulesets.in_extraconf_hostlist(["host1", "host2"], "host1") is True

    assert tuple_rulesets.in_extraconf_hostlist(["host1"], "host1") is True
    assert tuple_rulesets.in_extraconf_hostlist(["!host1", "host1", "!host1"], "host1") is False
    assert tuple_rulesets.in_extraconf_hostlist(["!host1"], "host1") is False
    assert tuple_rulesets.in_extraconf_hostlist(["!host2"], "host1") is False
    assert tuple_rulesets.in_extraconf_hostlist(["host1", "!host2"], "host1") is True
    assert tuple_rulesets.in_extraconf_hostlist(["!host2", "host1"], "host1") is True
    assert tuple_rulesets.in_extraconf_hostlist(["~h"], "host1") is True
    assert tuple_rulesets.in_extraconf_hostlist(["~h"], "host1") is True
    assert tuple_rulesets.in_extraconf_hostlist(["~h$"], "host1") is False
    assert tuple_rulesets.in_extraconf_hostlist(["~1"], "host1") is False
    assert tuple_rulesets.in_extraconf_hostlist(["~.*1"], "host1") is True
    assert tuple_rulesets.in_extraconf_hostlist(["~.*1$"], "host1") is True


# TODO: in_binary_hostlist


def test_get_rule_options_regular_rule() -> None:
    options = {"description": 'Put all hosts into the contact group "all"'}
    entry: tuple[str, list[str], list[str], dict] = ("all", [], tuple_rulesets.ALL_HOSTS, options)
    assert tuple_rulesets.get_rule_options(entry) == (entry[:-1], options)


def test_get_rule_options_empty_options() -> None:
    options: dict = {}
    entry: tuple[str, list[str], list[str], dict] = ("all", [], tuple_rulesets.ALL_HOSTS, options)
    assert tuple_rulesets.get_rule_options(entry) == (entry[:-1], options)


def test_get_rule_options_missing_options() -> None:
    entry: tuple[str, list[str], list[str]] = ("all", [], tuple_rulesets.ALL_HOSTS)
    assert tuple_rulesets.get_rule_options(entry) == (entry, {})


def test_hosttags_match_taglist() -> None:
    assert tuple_rulesets.hosttags_match_taglist(["no-agent"], ["no-agent"])
    assert tuple_rulesets.hosttags_match_taglist(["no-agent", "test"], ["no-agent"])
    assert tuple_rulesets.hosttags_match_taglist(["no-agent", "test"], ["no-agent", "test"])


def test_hosttags_match_taglist_not_matching() -> None:
    assert not tuple_rulesets.hosttags_match_taglist(["no-agent"], ["test"])
    assert not tuple_rulesets.hosttags_match_taglist(["tag", "no-agent", "test2"], ["test"])
    assert not tuple_rulesets.hosttags_match_taglist(["no-agent", "test"], ["test", "tag3"])


def test_hosttags_match_taglist_negate() -> None:
    assert not tuple_rulesets.hosttags_match_taglist(["no-agent", "test"], ["no-agent", "!test"])
    assert tuple_rulesets.hosttags_match_taglist(["no-agent"], ["no-agent", "!test"])


@pytest.mark.parametrize(
    "service_patterns,service,expected",
    [
        ([], "Disk IO SUMMARY", False),
        ([""], "", True),
        ([""], "Disk IO SUMMARY", True),
        (["!"], "", True),
        (["!"], "Disk IO SUMMARY", True),
        (["!!"], "!", False),
        (["!!"], "a", True),
        (["$"], "", True),
        (["$"], "a", False),
        (["!$"], "", False),
        (["!$"], "a", True),
        (["."], "", False),
        (["."], "a", True),
        (["."], "aa", True),
        ([".$"], "aa", False),
        ([".*"], "", True),
        ([".*"], "Filesystem /", True),
        (["Interface 1"], "Interface 1", True),
        (["Interface 1"], "interface 1", False),
        (["!Filesystem /"], "Filesystem /", False),
        (["!Filesystem /"], "Filesystem /boot", False),
        (["!Filesystem /$"], "Filesystem /boot", True),
        (["Interface 1", "Interface 2"], "Interface 2", True),
        (["Interface 1", "Interface 2"], "Interface 22", True),
        (["Interface 1", "Interface 2"], "Interface 3", False),
        (["Interface 1", "!Interface 2", "Interface 3"], "Interface 2", False),
        (["Memory$"], "Mem", False),
        (["Memory$"], "Memory", True),
        (["Memory$"], "Memory used", False),
        (["OMD heute .*"], "OMD heute performance", True),
        (["OMD heute .*"], "OMD heute ", True),
        (["OMD heute .*"], "OMD heute", False),
        (["!^OMD .* performance$"], "OMD stable performance", False),
        ([r"OMD ([a-z]+) \1"], "OMD stable stable", True),
    ],
)
def test_in_extraconf_servicelist(
    service_patterns: list[str], service: str, expected: bool
) -> None:
    assert config.in_extraconf_servicelist(service_patterns, service) == expected
