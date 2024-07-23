"""Methods run on application start and shutdown."""
import logging


from litestar import Litestar
from sqlalchemy import Engine
from typing import cast
from src.database import create_sqlalchemy_engine, Base
from src.environment import Environment


logger = logging.getLogger(__name__)

def read_environment(app: Litestar) -> Environment:
    app.state.environment = Environment()
    logger.info("Reading environment... %s", app.state.environment)
    return cast("Environment", app.state.environment)


def get_db_connection(app: Litestar) -> Engine:
    if not getattr(app.state, "engine", None):
        logger.info("Creating sqlalchemy engine...")
        app.state.engine = create_sqlalchemy_engine(app.state.environment)
    return cast("Engine", app.state.engine)


def apply_db_metadata(app: Litestar) -> None:
    logger.info("Creating tables...")
    Base.metadata.create_all(app.state.engine)


def close_db_connection(app: Litestar) -> None:
    if getattr(app.state, "engine", None):
        cast("Engine", app.state.engine).dispose()
