# SPDX-FileCopyrightText: 2022-present Lennart Rathgeb <108350061+RathgebL@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

from os import path

SCRIPT_DIR = path.dirname(__file__)


def read_file(file: str) -> str:
    file_path = path.join(SCRIPT_DIR, file)
    file_buffer = open(file_path, "r")
    return file_buffer.read()
