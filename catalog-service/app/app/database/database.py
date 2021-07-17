from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..settings import DbSettings


db_type, db_server, db_name, db_user, db_pass = DbSettings().get_settings()
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"{db_type}://{db_user}:{db_pass}@{db_server}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
