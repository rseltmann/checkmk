#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import os
import time

import pytest

from tests.testlib import WatchLog
from tests.testlib.fixtures import web  # noqa: F401 # pylint: disable=unused-import
from tests.testlib.site import Site

from cmk.utils import version as cmk_version


@pytest.fixture(name="fake_sendmail")
def fake_sendmail_fixture(site: Site):
    site.write_text_file(
        "local/bin/sendmail", "#!/bin/bash\n" "set -e\n" 'echo "sendmail called with: $@"\n'
    )
    os.chmod(site.path("local/bin/sendmail"), 0o775)
    yield
    site.delete_file("local/bin/sendmail")


@pytest.fixture(
    name="test_log",
    params=[
        ("nagios", "var/log/nagios.log"),
        pytest.param(
            ("cmc", "var/check_mk/core/history"),
            marks=pytest.mark.skipif(
                cmk_version.is_raw_edition(), reason="CMC not supported on CRE"
            ),
        ),
    ],
)
def test_log_fixture(
    request, web, site: Site, fake_sendmail
):  # noqa: F811 # pylint: disable=redefined-outer-name
    core, log = request.param
    site.set_config("CORE", core, with_restart=True)

    users = {
        "hh": {
            "alias": "Harry Hirsch",
            "password": "1234",
            "email": "%s@localhost" % web.site.id,
            "contactgroups": ["all"],
        },
    }

    expected_users = set(["cmkadmin", "automation"] + list(users.keys()))
    web.add_htpasswd_users(users)
    all_users = web.get_all_users()
    assert not expected_users - set(all_users.keys())

    site.live.command("[%d] STOP_EXECUTING_HOST_CHECKS" % time.time())
    site.live.command("[%d] STOP_EXECUTING_SVC_CHECKS" % time.time())

    web.add_host(
        "notify-test",
        attributes={
            "ipaddress": "127.0.0.1",
        },
    )
    web.activate_changes()

    with WatchLog(site, log, default_timeout=20) as l:
        yield l

    site.live.command("[%d] START_EXECUTING_HOST_CHECKS" % time.time())
    site.live.command("[%d] START_EXECUTING_SVC_CHECKS" % time.time())

    web.delete_host("notify-test")
    web.delete_htpasswd_users(list(users.keys()))
    web.activate_changes()


def test_simple_rbn_host_notification(test_log, site: Site):
    site.send_host_check_result("notify-test", 1, "FAKE DOWN", expected_state=1)

    # NOTE: "] " is necessary to get the actual log line and not the external command execution
    test_log.check_logged(
        "] HOST NOTIFICATION: check-mk-notify;notify-test;DOWN;check-mk-notify;FAKE DOWN"
    )
    test_log.check_logged("] HOST NOTIFICATION: hh;notify-test;DOWN;mail;FAKE DOWN")
    test_log.check_logged(
        "] HOST NOTIFICATION RESULT: hh;notify-test;OK;mail;Spooled mail to local mail transmission agent;"
    )


def test_simple_rbn_service_notification(test_log, site: Site):
    site.send_service_check_result("notify-test", "PING", 2, "FAKE CRIT")

    # NOTE: "] " is necessary to get the actual log line and not the external command execution
    test_log.check_logged(
        "] SERVICE NOTIFICATION: check-mk-notify;notify-test;PING;CRITICAL;check-mk-notify;FAKE CRIT"
    )
    test_log.check_logged("] SERVICE NOTIFICATION: hh;notify-test;PING;CRITICAL;mail;FAKE CRIT")
    test_log.check_logged(
        "] SERVICE NOTIFICATION RESULT: hh;notify-test;PING;OK;mail;Spooled mail to local mail transmission agent;"
    )
