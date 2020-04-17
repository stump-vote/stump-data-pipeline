import os

from env import read_env_variables


path_to_env_file = os.environ.get('STUMP_DATA_ENV') or './.env'
env = read_env_variables(path_to_env_file)
