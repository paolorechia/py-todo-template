import logging
import os
from dataclasses import dataclass
from src.environment import Environment


logger = logging.getLogger(__name__)


@dataclass
class Secrets:
    username: str
    password: str


def read_secrets(environment: Environment) -> Secrets:
    logger.info("Reading secrets...")
    secrets_dict = {}
    for secret_name in Secrets.__dataclass_fields__.keys():
        secret_filepath = os.path.join(environment.secrets_config_filepath, secret_name)
        logger.info("Reading secret %s", secret_filepath)
        with open(secret_filepath, "r") as fp:
            secrets = fp.read()
            secrets_dict[secret_name] = secrets
    return Secrets(**secrets_dict)
