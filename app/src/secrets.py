from dataclasses import dataclass
from app.src.environment import Environment


@dataclass
class Secrets:
    username: str
    password: str


def read_secrets(environment: Environment) -> Secrets:
    with open(environment.secrets_config_filepath, "r"):
        raise NotImplementedError
