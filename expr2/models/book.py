"""
Simplified book model for experiment
"""

from sqlalchemy import Column, Integer, String
from db_init import Base

class Book(Base):
    """Book model."""
    
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title
        }
