"""
User model for Smart Library System.
Simple ORM model using SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db_init import Base

class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with borrowing history
    borrowings = relationship("Borrowing", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }
