from src.environment import Environment
from src.secrets import read_secrets
from sqlalchemy import create_engine, URL, Engine


def create_sqlalchemy_engine(environment: Environment) -> Engine:
    if environment.database_driver == "postgresql":
        secrets = read_secrets(environment)
        url_object = URL.create(
            "postgresql",
            username=secrets.username,
            password=secrets.password,
            host=environment.host,
            database=environment.database_name,
        )
        engine = create_engine(url_object)

    else:
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    return engine
