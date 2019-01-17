#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Age,
    Checkbox,
    Dictionary,
    MonitoringState,
    TextAscii,
    Tuple,
)
from cmk.gui.plugins.wato import (
    RulespecGroupCheckParametersApplications,
    register_check_parameters,
)

register_check_parameters(
    RulespecGroupCheckParametersApplications,
    "oracle_instance",
    _("Oracle Instance"),
    Dictionary(
        title=_("Consider state of Archivelogmode: "),
        elements=[
            ('archivelog',
             MonitoringState(
                 default_value=0,
                 title=_("State in case of Archivelogmode is enabled: "),
             )),
            (
                'noarchivelog',
                MonitoringState(
                    default_value=1,
                    title=_("State in case of Archivelogmode is disabled: "),
                ),
            ),
            (
                'forcelogging',
                MonitoringState(
                    default_value=0,
                    title=_("State in case of Force Logging is enabled: "),
                ),
            ),
            (
                'noforcelogging',
                MonitoringState(
                    default_value=1,
                    title=_("State in case of Force Logging is disabled: "),
                ),
            ),
            (
                'logins',
                MonitoringState(
                    default_value=2,
                    title=_("State in case of logins are not possible: "),
                ),
            ),
            (
                'primarynotopen',
                MonitoringState(
                    default_value=2,
                    title=_("State in case of Database is PRIMARY and not OPEN: "),
                ),
            ),
            ('uptime_min',
             Tuple(
                 title=_("Minimum required uptime"),
                 elements=[
                     Age(title=_("Warning if below")),
                     Age(title=_("Critical if below")),
                 ])),
            ('ignore_noarchivelog',
             Checkbox(
                 title=_("Ignore state of no-archive log"),
                 label=_("Enable"),
                 help=_("If active, only a single summary item is displayed. The summary "
                        "will explicitly mention sensors in warn/crit state but the "
                        "sensors that are ok are aggregated."),
                 default_value=False)),
        ],
    ),
    TextAscii(title=_("Database SID"), size=12, allow_empty=False),
    match_type="dict",
)
