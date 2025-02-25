#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
from __future__ import annotations

import signal
import time
from typing import TYPE_CHECKING

import pytest
from werkzeug.test import create_environ

from cmk.gui.exceptions import RequestTimeout
from cmk.gui.http import request
from cmk.gui.utils.timeout_manager import timeout_manager, TimeoutManager
from cmk.gui.wsgi.applications.checkmk import CheckmkApp
from cmk.gui.wsgi.type_defs import WSGIResponse

if TYPE_CHECKING:
    # TODO: Directly import from wsgiref.types in Python 3.11, without any import guard
    from _typeshed.wsgi import StartResponse, WSGIEnvironment


class CheckmkTestApp(CheckmkApp):
    def wsgi_app(self, environ: WSGIEnvironment, start_response: StartResponse) -> WSGIResponse:
        assert request.request_timeout == 110

        registered = signal.getsignal(signal.SIGALRM)
        assert callable(registered)
        assert registered.__name__ == "handle_request_timeout"

        assert signal.alarm(123) != 0
        timeout_manager.disable_timeout()
        assert signal.alarm(0) == 0
        return []


def make_start_response() -> StartResponse:
    def start_response(status, headers, exc_info=None):
        def start(output) -> None:  # type:ignore[no-untyped-def]
            return None

        return start

    return start_response


def test_checkmk_app_enables_timeout_handling() -> None:
    assert signal.alarm(0) == 0
    CheckmkTestApp()(create_environ(), make_start_response())
    assert signal.alarm(0) == 0


def test_timeout_manager_raises_timeout() -> None:
    tm = TimeoutManager()

    with pytest.raises(RequestTimeout):
        tm.enable_timeout(1)
        time.sleep(2)


def test_timeout_manager_disable() -> None:
    tm = TimeoutManager()

    tm.enable_timeout(1)
    tm.disable_timeout()
    time.sleep(1)
