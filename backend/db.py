# backend/db.py
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime


DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./intel.db')


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ProviderCred(Base):
__tablename__ = 'provider_creds'
id = Column(Integer, primary_key=True, index=True)
provider = Column(String(100), index=True)
name = Column(String(200), nullable=True)
encrypted_api_key = Column(LargeBinary, nullable=False)
meta = Column(Text, nullable=True)


class IngestedItem(Base):
__tablename__ = 'ingested_items'
id = Column(Integer, primary_key=True, index=True)
provider = Column(String(100))
raw = Column(Text)
summary = Column(Text, nullable=True)
created_at = Column(DateTime, default=datetime.utcnow)
forwarded = Column(Integer, default=0) # 0/1


class LogEntry(Base):
__tablename__ = 'logs'
id = Column(Integer, primary_key=True, index=True)
level = Column(String(20))
message = Column(Text)
ts = Column(DateTime, default=datetime.utcnow)


def init_db():
Base.metadata.create_all(bind=engine)