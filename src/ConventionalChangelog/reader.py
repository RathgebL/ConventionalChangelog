# SPDX-FileCopyrightText: 2022-present Lennart Rathgeb <108350061+RathgebL@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

from git import Commit, Repo
from semver import Version
import re

COMMIT_REGEX = re.compile(
    r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(?P<scope>\(\w+\)?((?=:\s)|(?=!:\s)))?(?P<breaking>!)?(?P<subject>:\s.*)?|^(?P<merge>Merge \w+)"
)


def get_description(message_parts, match_dict):
    if match_dict["subject"]:
        message_parts.pop(0)
        return match_dict["subject"].removeprefix(": ")
    else:
        return message_parts.pop(0)


def read_commit(commit: Commit):
    parts = commit.message.split("\n\n")
    parts[0] = parts[0].replace("\n", " ").strip()
    res = COMMIT_REGEX.match(parts[0])
    if res:
        match = res.groupdict()
        return {
            "hash": commit.hexsha,
            "type": match["type"] if match["type"] else "other",
            "scope": match["scope"],
            "description": get_description(parts, match),
            "body": parts.pop() if len(parts) > 0 else None,
            "footer": parts,
        }
    else:
        return {
            "hash": commit.hexsha,
            "type": "other",
            "scope": None,
            "description": parts[0],
            "body": parts.pop(0) if len(parts) > 0 else None,
            "footer": parts,
        }


def read_version_tags(repo):
    tags = []
    for tag in repo.tags:
        version_string = tag.name.removeprefix("v")
        if Version.isvalid(version_string):
            tags.append((Version.parse(version_string), tag.commit.hexsha))

    tags.sort()
    tags.append((None, repo.head.commit.hexsha))
    return tags


def read_repo(repo: Repo):
    versions = []
    commits = set()

    def commits_includes(commit):
        x = commits.isdisjoint([commit.hexsha])
        commits.add(commit.hexsha)
        return x

    for tag in read_version_tags(repo):
        version = {
            "semver": tag[0].to_dict() if tag[0] else None,
            "hash": tag[1],
            "commits": [],
        }

        unique_commits = filter(commits_includes, repo.iter_commits(tag[1]))

        for commit in unique_commits:
            commits.add(commit.hexsha)
            version["commits"].append(read_commit(commit))

        versions.append(version)

    return versions
