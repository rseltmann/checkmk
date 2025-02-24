#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.config import active_config
from cmk.gui.i18n import _
from cmk.gui.logged_in import user
from cmk.gui.plugins.dashboard.utils import get_permitted_dashboards
from cmk.gui.plugins.sidebar.utils import (
    footnotelinks,
    make_topic_menu,
    show_topic_menu,
    SidebarSnapin,
    snapin_registry,
)
from cmk.gui.type_defs import TopicMenuTopic


@snapin_registry.register
class Dashboards(SidebarSnapin):
    @staticmethod
    def type_name() -> str:
        return "dashboards"

    @classmethod
    def title(cls) -> str:
        return _("Dashboards")

    @classmethod
    def description(cls) -> str:
        return _("Links to all dashboards")

    def show(self) -> None:
        show_topic_menu(treename="dashboards", menu=self._get_dashboard_menu_items())

        links = []
        if user.may("general.edit_dashboards"):
            if active_config.debug:
                links.append((_("Export"), "export_dashboards.py"))
            links.append((_("Edit"), "edit_dashboards.py"))
            footnotelinks(links)

    def _get_dashboard_menu_items(self) -> list[TopicMenuTopic]:
        return make_topic_menu(
            [("dashboards", (k, v)) for k, v in get_permitted_dashboards().items()]
        )
