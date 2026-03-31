from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Database_url = ""

engine = create_engine(Database_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
