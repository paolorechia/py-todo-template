import logging

from src.environment import Environment
from src.secrets import read_secrets
from sqlalchemy import create_engine, URL, Engine, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Item(Base):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(30))
    new_column: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, status={self.status!r})"


def create_sqlalchemy_engine(environment: Environment) -> Engine:
    if environment.database_driver == "postgresql":
        logger.info("Setting up postgres database connection")
        secrets = read_secrets(environment)
        url_object = URL.create(
            "postgresql",
            username=secrets.username,
            password=secrets.password,
            host=environment.database_host,
            database=environment.database_name,
        )
        engine = create_engine(url_object)

    else:
        engine = create_engine(
            "sqlite:////tmp/test_app.db",
            echo=True,
        )

    return engine
