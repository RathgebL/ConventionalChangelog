# SPDX-FileCopyrightText: 2022-present Lennart Rathgeb <108350061+RathgebL@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

CHANGELOG_HEADER = """# Change Log

All notable changes to this project will be documented in this file.

"""


def semver_to_string(version):
    # a semver version includes always major.minor.patch
    result = "{}.{}.{}".format(version["major"], version["minor"], version["patch"])
    # optional prerelease suffix
    result += ("-" + version["prerelease"]) if version["prerelease"] else ""
    # optional build suffix
    result += ("+" + version["build"]) if version["build"] else ""
    return result


def write_changelog(versions):
    versions.reverse()
    result = CHANGELOG_HEADER

    for version in versions:
        # version["semver"] is None for the latest unreleased commits
        if version["semver"]:
            result += semver_to_string(version["semver"])
        for commit in version["commits"]:
            result += "- **{}**: {}\n".format(commit["type"], commit["description"])
        result += "\n"

    # Remove final newline
    return result[:-1]
