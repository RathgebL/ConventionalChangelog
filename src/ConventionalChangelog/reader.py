# SPDX-FileCopyrightText: 2022-present Lennart Rathgeb <108350061+RathgebL@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

import re
from typing import Set
from git.repo.base import Repo
from git.objects.commit import Commit
from semver.version import Version
from ConventionalChangelog import _types

COMMIT_REGEX = re.compile(
    r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(?P<scope>\(\w+\)?((?=:\s)|(?=!:\s)))?(?P<breaking>!)?(?P<subject>:\s.*)?|^(?P<merge>Merge \w+)"
)


def semver_to_dict(version: Version) -> _types.SemVerDict:
    return {
        "major": version.major,
        "minor": version.minor,
        "patch": version.patch,
        "prerelease": version.prerelease,
        "build": version.build,
    }


def read_commit(commit: Commit) -> _types.CommitDict:
    parts = str(commit.message).split("\n\n")
    first_line = parts.pop(0).replace("\n", " ").strip()
    res = COMMIT_REGEX.match(first_line)
    if res:
        match = res.groupdict()
        return {
            "hash": commit.hexsha,
            "type": match["type"] if match["type"] else "other",
            "scope": match["scope"],
            "description": match["subject"].removeprefix(": ")
            if match["subject"]
            else first_line,
            "body": parts.pop(0) if len(parts) > 0 else None,
            "footer": parts,
        }
    else:
        return {
            "hash": commit.hexsha,
            "type": "other",
            "scope": None,
            "description": first_line,
            "body": parts.pop(0) if len(parts) > 0 else None,
            "footer": parts,
        }


def read_version_tags(repo: Repo) -> list[tuple[Version | None, str]]:
    tags: list[tuple[Version | None, str]] = []
    for tag in repo.tags:
        version_string = tag.name.removeprefix("v")
        if Version.isvalid(version_string):
            tags.append((Version.parse(version_string), tag.commit.hexsha))

    tags.sort()
    tags.append((None, repo.head.commit.hexsha))
    return tags


def read_repo(repo: Repo) -> list[_types.VersionDict]:
    versions = []
    commits: Set[str] = set()

    def commits_includes(commit: Commit) -> bool:
        x = commits.isdisjoint([commit.hexsha])
        commits.add(commit.hexsha)
        return x

    for tag in read_version_tags(repo):
        version: _types.VersionDict = {
            "semver": semver_to_dict(tag[0]) if tag[0] else None,
            "hash": tag[1],
            "commits": [],
        }

        unique_commits = filter(commits_includes, repo.iter_commits(tag[1]))

        for commit in unique_commits:
            commits.add(commit.hexsha)
            version["commits"].append(read_commit(commit))

        versions.append(version)

    return versions
