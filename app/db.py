from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import os
import dotenv

dotenv.load_dotenv()

engine = create_engine(os.getenv("DB_URL") or "sqlite:///./test.db")
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
