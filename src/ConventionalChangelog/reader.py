from git import Commit, Repo
import semver
import re

COMMIT_REGEX = re.compile(
    "^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(?P<scope>\(\w+\)?((?=:\s)|(?=!:\s)))?(?P<breaking>!)?(?P<subject>:\s.*)?|^(?P<merge>Merge \w+)"
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


def read_repo(repo: Repo):
    tags = []
    for tag in repo.tags:
        if semver.Version.isvalid(tag.name.removeprefix("v")):
            tags.append(
                (semver.Version.parse(tag.name.removeprefix("v")), tag.commit.hexsha)
            )
    tags.sort()
    prev = tags[len(tags) - 1]
    next_version = semver.Version(prev[0].major + 1, 0, 0)
    tags.append((next_version, repo.head.commit.hexsha))

    versions = []
    commits = set()

    for tag in tags:
        version = {
            "semver": tag[0].to_dict() if tag[0] != next_version else None,
            "hash": tag[1],
            "commits": [],
        }
        la = list(
            filter(lambda x: commits.isdisjoint([x.hexsha]), repo.iter_commits(tag[1]))
        )
        for li in la:
            commits.add(li.hexsha)
            version["commits"].append(read_commit(li))

        versions.append(version)

    return versions
