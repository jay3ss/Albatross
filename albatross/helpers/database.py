from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from albatross.settings import config
from albatross.core.models import Base


engine = create_engine(config.database_uri)


@contextmanager
def get_session(engine: Engine = None) -> Session:
    """
    Yields a database session and handles any issues with committing or rolling
    back changes.

    Parameters:
    engine (Engine): the database engine

    Yields:
        The database session.
    """
    if not engine:
        engine = get_engine()

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_database(engine: Engine):
    """Creates the database tables for the given engine if they don't already
    exist.

    Parameters:
        engine (sqlalchemy.engine.Engine): The database engine to use.
    """
    Base.metadata.create_all(bind=engine, checkfirst=True)


def get_engine() -> Engine:
    """Returns a SQLAlchemy engine instance.

    Returns:
        Engine: The SQLAlchemy engine instance.
    """
    return create_engine(config.database_uri)


create_database(get_engine())
