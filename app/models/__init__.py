from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import Config


Base = declarative_base()


def row_to_dict(row):
    if row is None:
        return None

    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d


@contextmanager
def session_scope():
    engine = create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
    )
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
