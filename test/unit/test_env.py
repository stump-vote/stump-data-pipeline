import os

import pytest

from env import read_env_variables


@pytest.fixture()
def environment():
    path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'data',
        '.env.unittest',
    ))
    env = read_env_variables(path)
    return env


def test_read_environment_variables(environment):
    assert environment.news_api_key == 'test_api_key'


def test_reference_missing_environment_variable(environment):
    with pytest.raises(AttributeError):
        environment.missing_var
