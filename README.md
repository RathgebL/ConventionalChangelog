# Conventional Changelog

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://spdx.org/licenses/MIT.html)
[![Latest Release](https://img.shields.io/github/v/release/RathgebL/ConventionalChangelog?display_name=tag&include_prereleases&sort=semver)](https://github.com/RathgebL/ConventionalChangelog/releases)

---

**Tool to generate changelogs from a project's commit messages and tags.**

This tool was written for my fundamentals of programming course at uni.

---

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Roadmap](#roadmap)
- [Installation](#installation)
- [License](#license)

## Installation

### Step 1: Install following software on your device

- [git](https://git-scm.com/)
- [python](https://python.org/)
- [pip](https://pip.pypa.io)

### Step 2: Clone the contents of this repository with git.

```shell
$ git clone https://github.com/RathgebL/ConventionalChangelog.git
$ cd ConventionalChangelog
```

### Step 3: Install Conventional Changelog with pip

```shell
$ pip install .
```

## Usage

When in a git repository run:

```shell
$ conventional-changelog
```

> Note:
> 
> This only works well if you
> - follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) style guide
> -  annotate your software versions with git tags following [Semantic Versioning](http://semver.org/) (example: `v3.24.8-beta`)

## Running Tests

To run tests, run the following commands:

```shell
$ pip install hatch
$ hatch run pytest
```

## Roadmap

- Sort commits per type
- Add config file support

## License

`conventionalchangelog` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
