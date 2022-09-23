import json
from os import path

SCRIPT_DIR = path.dirname(__file__)


def read_file(file: str) -> str:
    file_path = path.join(SCRIPT_DIR, file)
    file = open(file_path, "r")
    return file.read()