"""
Borrowing model for Smart Library System.
Simple ORM model using SQLAlchemy.
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db_init import Base

class Borrowing(Base):
    """Borrowing history model."""
    
    __tablename__ = "borrowings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")
    
    def __repr__(self):
        return f"<Borrowing(id={self.id}, user_id={self.user_id}, book_id={self.book_id})>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'borrowed_at': self.borrowed_at,
            'returned_at': self.returned_at
        }
