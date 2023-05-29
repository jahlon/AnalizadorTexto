import os
from importlib.resources import files
from pathlib import Path

import pytest


def invoke_tests():
    directory = str(files('analizador').joinpath(Path("entregas")))
    file_list = os.listdir(directory)

    for file in file_list:
        if not file.startswith("__"):
            pytest.main(["test_analizador.py", "--module-file", f"{directory}{os.sep}{file}", "--name", file])


if __name__ == "__main__":
    invoke_tests()
