from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URL = "sqlite:///./folder.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def init_DB():
    Base.metadata.create_all(bind=engine)
