from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:root@localhost:3306/staffpims'

# Install pymysql as the MySQL connector

engine = create_engine(SQLALCHEMY_DATABASE_URL)
meta = MetaData()
Base = declarative_base(bind=engine, metadata=meta)
conn = engine.connect()

# Create a session factory
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Additional utility function to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()