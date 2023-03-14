import pytest

import beaker
from examples.c2c import demo, main, sub
from tests.conftest import check_application_artifacts_output_stability


def test_demo() -> None:
    demo.demo()


@pytest.mark.parametrize("app", [main.app, sub.app])
def test_output_stability(app: beaker.Application) -> None:
    check_application_artifacts_output_stability(app, dir_per_test_file=False)
