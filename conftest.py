from pytest import fixture

def pytest_addoption(parser):
    parser.addoption("--model", action="store", default="")


@fixture()
def model(request):
    return request.config.getoption("--model")
