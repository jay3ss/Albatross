from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from albatross.core.models import Article, Author, Base
from albatross.core.schemas import ArticleCreate, ArticleUpdate
from albatross.settings import config

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


def get_article_by_id(article_id: int, db: Session = None) -> Article:
    """
    Get an article from the database by its ID

    Args:
        article_id (int): article's ID
        db (Session, optional): database session. Defaults to None.

    Returns:
        Article: the article with the given ID
    """
    if not db:
        db = get_session()
    article = db.query(Article).filter(Article.id == article_id).first()
    return article


def get_articles(limit: int = None, db: Session = None) -> list:
    """
    Gets all articles

    Args:
        limit (int, optional): max number of Articles. Defaults to None.
        db (Session, optional): database session. Defaults to None.

    Returns:
        list: list of Articles
    """
    if limit:
        return db.query(Article).limit(limit).all()
    else:
        return db.query(Article).all()


def delete_article(article_id: int, db: Session = None) -> None:
    """
    Deletes the article with the given ID

    Args:
        article_id (int): article's ID
        db (Session, optional): database session. Defaults to None.
    """
    if not db:
        db = get_session()
    article = get_article_by_id(article_id=article_id, db=db)
    db.delete(article)


def create_article(article: ArticleCreate, db: Session = None) -> None:
    """
    Creates a new article

    Args:
        article (ArticleCreate): the article Pydantic schema object
        db (Session, optional): database session. Defaults to None.
    """
    if not db:
        db = get_session()

    new_article = Article(
        title=article.title,
        author_id=article.author_id,
        content=article.content,
        summary=article.summary,
        image_url=article.image_url
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)


def update_article(article: ArticleUpdate, db: Session = None) -> Article:
    """
    Updates an article

    Args:
        article (ArticleCreate): the article Pydantic schema object
        db (Session, optional): database session. Defaults to None.

    Returns:
        Article: the updated article
    """
    if not db:
        db = get_session()

    db_article = get_article_by_id(article_id=article.id, db=db)
    for field, value in article:
        setattr(db_article, field, value)

    db.commit()
    db.refresh(db_article)
    return db_article


def get_author_by_id(author_id: int, db: Session = None) -> Author:
    """
    Get an author from the database by its ID

    Args:
        author_id (int): author's ID
        db (Session, optional): database session. Defaults to None.

    Returns:
        Author: the author with the given ID
    """
    if not db:
        db = get_session()

    author = db.query(Author).filter_by(id=author_id).first()
    return author


create_database(get_engine())
