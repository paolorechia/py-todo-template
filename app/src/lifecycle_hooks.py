"""Methods run on application start and shutdown."""

from litestar import Litestar
from sqlalchemy import Engine
from typing import cast
from src.database import create_sqlalchemy_engine
from src.environment import Environment


def read_environment(app: Litestar) -> Environment:
    app.state.environment = Environment()
    return cast("Environment", app.state.environment)


def get_db_connection(app: Litestar) -> Engine:
    if not getattr(app.state, "engine", None):
        app.state.engine = create_sqlalchemy_engine(app.state.environment)
    return cast("Engine", app.state.engine)


def close_db_connection(app: Litestar) -> None:
    if getattr(app.state, "engine", None):
        cast("Engine", app.state.engine).dispose()
