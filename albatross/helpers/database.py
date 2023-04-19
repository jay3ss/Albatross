# from sqlalchemy import create_engine
# from sqlalchemy.engine import Engine
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import Session, sessionmaker
# from sqlalchemy.pool import QueuePool

# from albatross.core.models import Article, Author, Base
# from albatross.core.schemas import (ArticleCreate, ArticleUpdate,
#                                     AuthorCreate, AuthorUpdate)
# from config import config


# engine = create_engine(config.database_uri, poolclass=QueuePool)
# Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# session = Session()


# def create_database(engine: Engine):
#     """Creates the database tables for the given engine if they don't already
#     exist.

#     Parameters:
#         engine (sqlalchemy.engine.Engine): The database engine to use.
#     """
#     Base.metadata.create_all(bind=engine, checkfirst=True)


# def get_engine() -> Engine:
#     """Returns a SQLAlchemy engine instance.

#     Returns:
#         Engine: The SQLAlchemy engine instance.
#     """
#     return create_engine(config.database_uri)


# def get_article_by_id(article_id: int, db: Session = None) -> Article:
#     """
#     Get an article from the database by its ID

#     Args:
#         article_id (int): article's ID
#         db (Session, optional): database session. Defaults to None.

#     Returns:
#         Article: the article with the given ID
#     """
#     if not db:
#         db = session
#     article = db.query(Article).filter(Article.id == article_id).first()
#     return article


# def get_articles(limit: int = None, db: Session = None) -> list:
#     """
#     Gets all articles

#     Args:
#         limit (int, optional): max number of Articles. Defaults to None.
#         db (Session, optional): database session. Defaults to None.

#     Returns:
#         list: list of Articles
#     """
#     if not db:
#         db = session

#     results = db.query(Article).limit(limit).all()
#     return results


# def delete_article(article_id: int, db: Session = None) -> None:
#     """
#     Deletes the article with the given ID

#     Args:
#         article_id (int): article's ID
#         db (Session, optional): database session. Defaults to None.
#     """
#     if not db:
#         db = session

#     try:
#         article = get_article_by_id(article_id=article_id, db=db)
#         db.delete(article)
#         db.commit()
#     except SQLAlchemyError as e:
#         raise e
#         db.rollback()
#     finally:
#         db.close()


# def create_article(article: ArticleCreate, db: Session = None) -> None:
#     """
#     Creates a new article

#     Args:
#         article (ArticleCreate): the article Pydantic schema object
#         db (Session, optional): database session. Defaults to None.
#     """
#     if not db:
#         db = session

#     new_article = Article(
#         title=article.title,
#         author_id=article.author_id,
#         content=article.content,
#         summary=article.summary,
#         image_url=article.image_url
#     )
#     try:
#         db.add(new_article)
#         db.commit()
#         db.refresh(new_article)
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise e
#     finally:
#         db.close()

#     return new_article


# def update_article(article: ArticleUpdate, db: Session = None) -> Article:
#     """
#     Updates an article

#     Args:
#         article (ArticleCreate): the article Pydantic schema object
#         db (Session, optional): database session. Defaults to None.

#     Returns:
#         Article: the updated article
#     """
#     if not db:
#         db = session

#     try:
#         db_article = get_article_by_id(article_id=article.id, db=db)
#         if db_article:
#             for field, value in article:
#                 setattr(db_article, field, value)
#             db.commit()
#             db.refresh(db_article)
#             return db_article
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise e
#     finally:
#         db.close()


# def get_author_by_id(author_id: int, db: Session = None) -> Author:
#     """
#     Get an author from the database by its ID

#     Args:
#         author_id (int): author's ID
#         db (Session, optional): database session. Defaults to None.

#     Returns:
#         Author: the author with the given ID
#     """
#     if not db:
#         db = session

#     author = db.query(Author).filter_by(id=author_id).first()
#     return author


# def get_authors(limit: int = None, db: Session = None) -> list:
#     """
#     Gets all authors

#     Args:
#         limit (int), optional): max number of authors. Defaults to None.
#         db (Session, optional): database session. Defaults to None.

#     Returns:
#         list: the authors
#     """
#     if not db:
#         db = session

#     return db.query(Author).limit(limit).all()


# def create_author(author: AuthorCreate, db: Session = None) -> Author:
#     """
#     Get an author from the database by its ID

#     Args:
#         author_id (int): author's ID
#         db (Session, optional): database session. Defaults to None.

#     Returns:
#         Author: the author with the given ID
#     """
#     if not db:
#         db = session

#     new_author = Author(name=author.name)

#     try:
#         db.add(new_author)
#         db.commit()
#         db.refresh(new_author)
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise e
#     finally:
#         db.rollback()

#     return new_author


# def update_author(author: AuthorUpdate, db: Session = None) -> Author:
#     """
#     Updates the author

#     Args:
#         author (AuthorUpdate): the author to update
#         db (Session, optional): database session. Defaults to None.

#     Returns:
#         Author: updated author
#     """
#     if not db:
#         db = session

#     db_author = get_author_by_id(author_id=author.id, db=db)
#     for field, value in author:
#         setattr(db_author, field, value)

#     db.commit()
#     db.refresh(db_author)
#     return db_author


# def delete_author(author_id: int, db: Session = None) -> bool:
#     """
#     Deletes an author. Returns True if the author existed (and was successfully
#     deleted), False otherwise

#     Args:
#         author_id (int): the ID of the author to be deleted
#         db (Session, optional): database session. Defaults to None.

#     Returns:
#         bool: Returns True if the author existed (and was successfully deleted),
#         False otherwise
#     """
#     if not db:
#         db = session

#     author = get_author_by_id(author_id=author_id, db=db)
#     if author:
#         db.delete(author)
#         db.commit()
#         return True

#     return False


# create_database(get_engine())
