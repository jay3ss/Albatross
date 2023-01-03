from contextlib import contextmanager

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from config import config
import sql_models as sm


engine = create_engine(config.database_uri)


@contextmanager
def get_session() -> Session:
    """
    Yields a database session and handles any issues with committing or rolling back changes.

    Yields:
        The database session.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def create_database(engine: Engine):
    """Creates the database if it does not exist.

    Args:
        engine: The SQLAlchemy engine to use to create the database.
    """

    inspector = inspect(engine)

    if not inspector.has_table("posts"):
        # Create the posts table
        sm.Post.metadata.create_all(bind=engine)
    if not inspector.has_table("authors"):
        # Create the authors table
        sm.Author.metadata.create_all(bind=engine)


create_database(engine)

if __name__ == "__main__":
    import sql_models as sm

    with get_session() as session:
        author = sm.Author("jayess")
        session.add(author)
