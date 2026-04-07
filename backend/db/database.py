from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings # Import settings to access DATABASE_URL

# For SQLite, adjust for other databases
engine = create_engine(
    
       settings.DATABASE_URL

)

# Create a configured "Session" class and a session instance for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models to inherit from
Base = declarative_base() 

# Dependency to get a database session, can be used in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create database tables based on the defined models
def create_tables():
    """Create database tables based on the defined models."""
    Base.metadata.create_all(bind=engine)
