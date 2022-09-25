# SPDX-FileCopyrightText: 2022-present Lennart Rathgeb <108350061+RathgebL@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

import json
from git.repo.base import Repo

from ConventionalChangelog.reader import read_repo
from tests.utils import read_file

# small public archive using conventional commits:
URL = "https://github.com/conventional-commits/conventional-commits-action.git"


def test_reader(tmp_path: str) -> None:
    repo = Repo.clone_from(URL, tmp_path)
    expected = json.loads(read_file("./small_archive/data.json"))
    result = read_repo(repo)
    assert result == expected
