from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Translation(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///translations.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
