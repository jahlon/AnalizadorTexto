import os
from importlib.resources import files

import pytest


def invoke_tests():
    directory = str(files('analizador.modelo'))
    file = "analizador.py"
    pytest.main(["test_analizador.py", "--module-file", f"{directory}{os.sep}{file}", "--name", file])


if __name__ == "__main__":
    invoke_tests()
