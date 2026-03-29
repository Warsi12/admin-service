import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Encode password to handle special characters like '@'
password = urllib.parse.quote_plus("Faraz@880730")
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres.iszmckganwvrpzewtiyh:password@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"connect_timeout": 10}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
