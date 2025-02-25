#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# fmt: off
# type: ignore

checkname = 'dotnet_clrmemory'

info = [[
    'AllocatedBytesPersec', 'Caption', 'Description', 'FinalizationSurvivors',
    'Frequency_Object', 'Frequency_PerfTime', 'Frequency_Sys100NS', 'Gen0heapsize',
    'Gen0PromotedBytesPerSec', 'Gen1heapsize', 'Gen1PromotedBytesPerSec', 'Gen2heapsize',
    'LargeObjectHeapsize', 'Name', 'NumberBytesinallHeaps', 'NumberGCHandles',
    'NumberGen0Collections', 'NumberGen1Collections', 'NumberGen2Collections',
    'NumberInducedGC', 'NumberofPinnedObjects', 'NumberofSinkBlocksinuse',
    'NumberTotalcommittedBytes', 'NumberTotalreservedBytes', 'PercentTimeinGC',
    'PercentTimeinGC_Base', 'ProcessID', 'PromotedFinalizationMemoryfromGen0',
    'PromotedMemoryfromGen0', 'PromotedMemoryfromGen1', 'Timestamp_Object',
    'Timestamp_PerfTime', 'Timestamp_Sys100NS'
],
        [
            '46584024', '', '', '201', '0', '3914064', '10000000', '6291456', '1110904',
            '1100372', '850168', '3279916', '73912', '_Global_', '4454200', '1470', '4',
            '3', '1', '0', '39', '135', '10493952', '33546240', '3003926', '-1', '0',
            '15076', '1110904', '850168', '0', '9918361461', '131261124692120000'
        ],
        [
            '0', '', '', '0', '0', '3914064', '10000000', '0', '0', '0', '0', '0', '0',
            'isa', '0', '41', '0', '0', '0', '0', '0', '8', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '9918361461', '131261124692120000'
        ],
        [
            '0', '', '', '0', '0', '3914064', '10000000', '0', '0', '0', '0', '0', '0',
            'SCNotification', '0', '390', '0', '0', '0', '0', '0', '65', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '9918361461', '131261124692120000'
        ],
        [
            '23292012', '', '', '201', '0', '3914064', '10000000', '6291456', '1110904',
            '1100372', '850168', '3279916', '73912', 'IAStorDataMgrSvc', '4454200', '678',
            '4', '3', '1', '0', '39', '30', '10493952', '33546240', '162041', '46336747',
            '5804', '15076', '1110904', '850168', '0', '9918361461', '131261124692120000'
        ],
        [
            '0', '', '', '0', '0', '3914064', '10000000', '0', '0', '0', '0', '0', '0',
            'CcmExec', '0', '21', '0', '0', '0', '0', '0', '2', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '9918361461', '131261124692120000'
        ],
        [
            '0', '', '', '0', '0', '3914064', '10000000', '0', '0', '0', '0', '0', '0',
            'IAStorIcon', '0', '340', '0', '0', '0', '0', '0', '30', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '9918361461', '131261124692120000'
        ]]

discovery = {'': [('_Global_', 'dotnet_clrmemory_defaultlevels')]}

checks = {
    '': [
        ('_Global_', {"upper": (10.0, 15.0)}, [
            (0, 'Time in GC: 0.07%', [
                ('percent', 0.06994060242314372, 10.0, 15.0, 0, 100),
            ]),
        ]),
    ],
}
