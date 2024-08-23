import datetime
from pathlib import Path
from typing import Any, Generator, Tuple, Type, TypeVar

from fastapi import HTTPException
from fastapi.logger import logger
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, as_declarative, scoped_session, sessionmaker
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime

from app.settings import settings

# DB CONNECTION ----------------------------------------------------------------
engine = create_engine(
    str(settings.db_url),
    pool_timeout=10,
    connect_args={
        "connect_timeout": 10,
    },
    pool_pre_ping=True,  # check connection before using
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db() -> Generator[Session, None, None]:
    """Dependency for FastAPI Routes.
    Generates a DB session to use in each request.

    Yields:
        Session: Database Session
    """
    session = scoped_session(session_factory)()
    try:
        yield session
        session.commit()
    except HTTPException:
        # This is a controlled exception. No need to log it.
        session.rollback()
        raise
    except Exception as e:
        logger.exception(f"Exception while attempting to commit session: {repr(e)}")
        session.rollback()
        raise
    finally:
        session.close()


# DB MODEL BASE CLASS ----------------------------------------------------------

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

meta = MetaData(naming_convention=convention)

Self = TypeVar("Self", bound="Base")


# class for views
ViewBase = declarative_base()


@as_declarative(metadata=meta)
class Base:
    """
    Base for all models.
    """

    __tablename__: str
    __table__: Table
    __table_args__: Tuple[Any, ...]

    # Add created and updated timestamps to all tables/models
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(),
        onupdate=datetime.datetime.now(),
    )

    @classmethod
    def get(cls: Type[Self], session: Session, ident: Any) -> Self:
        """Return an instance based on the given primary key identifier,
        or ``None`` if not found.
        E.g.::
            my_user = User.get(session, 5)
        Args:
            session (Session): DB Connection.
            ident (Any): A scalar, tuple, or dictionary representing the
         primary key.  For a composite (e.g. multiple column) primary key,
         a tuple or dictionary should be passed.

        Returns:
            Any: The object instance, or ``None``.
        """
        return session.query(cls).get(ident)

    def to_dict(self, fields=None):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if not fields or column.name in fields
        }


# UTILITY FUNCTIONS ------------------------------------------------------------


def load_all_models() -> None:
    import importlib

    model_paths = Path(__file__).parent.glob("api/v1/**/models.py")
    for path in model_paths:
        module_name = "app." + ".".join(path.parts[path.parts.index("api") :]).rstrip(
            ".py",
        )
        importlib.import_module(module_name)
