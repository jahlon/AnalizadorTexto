import os
from importlib.resources import files
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption("--module-file", action="store", default="default name")
    parser.addoption("--name", action="store", default="default name")


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" or result.when == "setup":
        item.session.results[item] = result


def pytest_sessionfinish(session, exitstatus):
    results_by_test = dict()
    for result in session.results.values():
        test_name: str = result.nodeid.split("::")[1]
        index = test_name.find("[")
        if index > -1:
            key = test_name[:index]
        else:
            key = test_name

        if key in results_by_test.keys():
            results_by_test[key]["total"] += 1
            if result.outcome == "passed":
                results_by_test[key]["passed"] += 1
        else:
            results_by_test[key] = {"total": 1, "passed": 1 if result.outcome == "passed" else 0}

    report_file_name = session.config.getoption("--name")[:-3]
    path = Path(files("tests").joinpath(Path("resultados")))
    if not path.exists():
        os.mkdir(path)

    with open(f"{path}{os.sep}{report_file_name}.txt", mode="w", encoding="utf8") as file:
        total_tests = len(results_by_test)
        score_sum = 0
        line_char = u'\u2500' * 93
        c_char = u'\u2502'
        header = f"{line_char}\n{c_char}{'#':^3}{c_char}{' Prueba':<78}{c_char}{'Puntos':^8}{c_char}\n{line_char}\n"
        file.write(header)
        for count, item in enumerate(results_by_test.items(), start=1):
            key, value = item
            test_score = value["passed"] / value["total"]
            score_sum += test_score
            inter_test = f"({value['passed']}/{value['total']})"
            line = f"{c_char}{count:<3}{c_char} {key:<70}{inter_test:<7}{c_char}{test_score:^8.1f}{c_char}\n"
            file.write(line)

        file.write(f"{line_char}\n")
        footer = f"{c_char}{'TOTAL':<82}{c_char}{score_sum:^8.1f}{c_char}\n{line_char}\n"
        file.write(footer)
        score = score_sum / total_tests * 5
        file.write(f"NOTA: {score_sum:.1f} / {total_tests} = {score: .1f}")
