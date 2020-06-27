from io import BytesIO
from os.path import join, dirname, abspath

FIXTURES_DIR = "fixtures"


def load_file_data(filename: str, path: str = FIXTURES_DIR) -> tuple:
    return load_binary_file(filename, path), filename


def load_binary_file(filename: str, path: str = FIXTURES_DIR) -> BytesIO:
    with open(file_path(filename, path), "rb") as data:
        return BytesIO(data.read())


def file_path(filename: str, path: str = FIXTURES_DIR) -> str:
    relative_path = join(dirname(__file__), path)
    absolute_path = abspath(relative_path)

    return join(absolute_path, filename)
