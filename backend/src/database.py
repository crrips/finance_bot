from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

database_url = 'postgresql+psycopg2://user:password@db:5432/finance_db'
engine = create_engine(database_url)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        