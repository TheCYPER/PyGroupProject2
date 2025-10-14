"""
Library class for Smart Library System.
Simple interface for library operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from datetime import datetime
from db_init import get_session, close_session
from models.book import Book
from models.user import User
from models.borrowing import Borrowing

class Library:
    """Simple library interface."""
    
    def __init__(self):
        self.name = "Smart Library System"
    
    # Book operations
    def add_book(self, title: str, author: str, genre: str, year: int, rating: float) -> dict:
        """Add a new book."""
        session = get_session()
        try:
            book = Book(title=title, author=author, genre=genre, year=year, rating=rating)
            session.add(book)
            session.commit()
            return book.to_dict()
        finally:
            close_session(session)
    
    def get_all_books(self) -> list[dict]:
        """Get all books."""
        session = get_session()
        try:
            books = session.query(Book).all()
            return [book.to_dict() for book in books]
        finally:
            close_session(session)
    
    def search_books(self, keyword: str) -> list[dict]:
        """Search books by keyword."""
        session = get_session()
        try:
            books = session.query(Book).filter(
                or_(
                    Book.title.contains(keyword),
                    Book.author.contains(keyword),
                    Book.genre.contains(keyword)
                )
            ).all()
            return [book.to_dict() for book in books]
        finally:
            close_session(session)
    
    def get_top_rated_books(self, limit: int = 10) -> list[dict]:
        """Get top-rated books."""
        session = get_session()
        try:
            books = session.query(Book).order_by(desc(Book.rating)).limit(limit).all()
            return [book.to_dict() for book in books]
        finally:
            close_session(session)
    
    # User operations
    def add_user(self, name: str) -> dict:
        """Add a new user."""
        session = get_session()
        try:
            user = User(name=name)
            session.add(user)
            session.commit()
            return user.to_dict()
        finally:
            close_session(session)
    
    def get_all_users(self) -> list[dict]:
        """Get all users."""
        session = get_session()
        try:
            users = session.query(User).all()
            return [user.to_dict() for user in users]
        finally:
            close_session(session)
    
    # Borrowing operations
    def borrow_book(self, user_id: int, book_id: int) -> bool:
        """Borrow a book."""
        session = get_session()
        try:
            borrowing = Borrowing(user_id=user_id, book_id=book_id)
            session.add(borrowing)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            close_session(session)
    
    def return_book(self, user_id: int, book_id: int) -> bool:
        """Return a book."""
        session = get_session()
        try:
            borrowing = session.query(Borrowing).filter(
                Borrowing.user_id == user_id,
                Borrowing.book_id == book_id,
                Borrowing.returned_at.is_(None)
            ).first()
            
            if borrowing:
                borrowing.returned_at = datetime.utcnow()
                session.commit()
                return True
            return False
        except Exception:
            session.rollback()
            return False
        finally:
            close_session(session)
    
    def get_user_borrowed_books(self, user_id: int) -> list[dict]:
        """Get user's currently borrowed books."""
        session = get_session()
        try:
            borrowings = session.query(Borrowing).join(Book).filter(
                Borrowing.user_id == user_id,
                Borrowing.returned_at.is_(None)
            ).all()
            
            books = []
            for borrowing in borrowings:
                book = session.query(Book).filter(Book.id == borrowing.book_id).first()
                if book:
                    books.append(book.to_dict())
            return books
        finally:
            close_session(session)
    
    def get_statistics(self) -> dict:
        """Get library statistics."""
        session = get_session()
        try:
            total_books = session.query(Book).count()
            total_users = session.query(User).count()
            
            # Get average rating
            avg_rating = session.query(Book.rating).all()
            avg_rating = sum(r[0] for r in avg_rating) / len(avg_rating) if avg_rating else 0
            
            return {
                'total_books': total_books,
                'total_users': total_users,
                'average_rating': round(avg_rating, 2)
            }
        finally:
            close_session(session)
