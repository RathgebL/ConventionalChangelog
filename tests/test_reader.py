import json
from git import Repo

from ConventionalChangelog.reader import read_repo
from tests.utils import read_file

# small public archive using conventional commits:
URL = "https://github.com/conventional-commits/conventional-commits-action.git"


def test_reader(tmp_path):
    repo = Repo.clone_from(URL, tmp_path)
    expected = json.loads(read_file("./small_archive/data.json"))
    result = read_repo(repo)
    assert result == expected
