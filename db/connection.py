from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    print("db연결 시작")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("db 종료")