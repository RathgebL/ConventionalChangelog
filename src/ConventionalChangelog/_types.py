from typing import Optional, TypedDict


class SemVerDict(TypedDict):
    major: int
    minor: int
    patch: int
    prerelease: Optional[str]
    build: Optional[str]


class CommitDict(TypedDict):
    hash: str
    type: str
    scope: Optional[str]
    description: str
    body: Optional[str]
    footer: list[str]


class VersionDict(TypedDict):
    semver: Optional[SemVerDict]
    hash: str
    commits: list[CommitDict]
