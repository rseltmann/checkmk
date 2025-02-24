#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# fmt: off
# type: ignore



checkname = 'liebert_fans_condenser'


info = [['How funny is this', '4.2', 'out of 10 clowns']]


discovery = {'': [('How funny is this', {})]}


checks = {
    '': [
        ('How funny is this', {'levels_lower': (8, 9), 'levels': (80, 90)}, [
            (2, '4.20 out of 10 clowns (warn/crit below 8.00 out of 10 clowns/9.00 out of 10 clowns)', [
                ('filehandler_perc', 4.2, 80, 90, None, None),
            ]),
        ]),
    ],
}
