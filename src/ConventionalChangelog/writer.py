# SPDX-FileCopyrightText: 2022-present Lennart Rathgeb <108350061+RathgebL@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

from string import Template


def write_changelog(versions):
    versions.reverse()
    a = "# Change Log\n\nAll notable changes to this project will be documented in this file.\n\n"

    for version in versions:
        v = version["semver"]
        if v:
            a += Template("## [${major}.${minor}.${patch}").substitute(
                major=v["major"], minor=v["minor"], patch=v["patch"])
            if v["prerelease"]:
                a += "-" + v["prerelease"]
            if v["build"]:
                a += "+" + v["build"]
            a += "]\n\n"
        for commit in version["commits"]:
            a = a + "- **"+commit["type"]+"**: "+commit["description"]+"\n"
        a = a + "\n"
    return a[:-1]