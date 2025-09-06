
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.base import Base

DATABASE_URL = "sqlite:///app.db"

engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
