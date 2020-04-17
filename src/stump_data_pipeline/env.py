import os

from dotenv import load_dotenv


class Environment(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def read_env_variables(filepath=None):
    if filepath is None:
        load_dotenv()
    else:
        load_dotenv(filepath)
    env = Environment(**os.environ)
    return env
