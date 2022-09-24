# SPDX-FileCopyrightText: 2022-present Lennart Rathgeb <108350061+RathgebL@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

import json
from ConventionalChangelog.writer import write_changelog
from tests.utils import read_file

def test_writer():
    data = json.loads(read_file("./small_archive/data.json"))
    expected = read_file("./small_archive/result.md")
    result = write_changelog(data)
    print(result)
    assert result == expected
