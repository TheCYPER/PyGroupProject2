"""
Database initialization for Smart Library System.
Simple ORM setup using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create base class for all models
Base = declarative_base()

# Database setup
engine = create_engine('sqlite:///library.db', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables."""
    Base.metadata.drop_all(engine) # restart everytime
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def get_session():
    """Get database session."""
    return SessionLocal()

def close_session(session):
    """Close database session."""
    session.close()
