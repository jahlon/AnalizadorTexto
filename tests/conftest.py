def pytest_addoption(parser):
    parser.addoption("--module-file", action="store", default="default name")
    parser.addoption("--name", action="store", default="default name")


def pytest_sessionstart(session):
    session.results = dict()
