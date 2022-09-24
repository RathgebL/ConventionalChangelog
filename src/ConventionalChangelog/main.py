# SPDX-FileCopyrightText: 2022-present Lennart Rathgeb <108350061+RathgebL@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

import json
import os
from sys import argv
from git import Repo
from ConventionalChangelog import reader
from ConventionalChangelog import writer


def main() -> None:
    path = path.abspath(argv[1]) if len(argv) > 1 else os.getcwd()
    repo = Repo(path)
    data = reader.read_repo(repo)
    changelog = writer.write_changelog(data)
    print(changelog)


if __name__ == "__main__":
    main()
