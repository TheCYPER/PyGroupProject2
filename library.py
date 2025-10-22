"""
Library class for Smart Library System.
Simple interface for library operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, func
from datetime import datetime
from collections import Counter
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
    
    def naive_search_books(self, keyword: str) -> list[dict]:
        """linear search using for loop"""
        session = get_session()
        try:
            results = []
            books = session.query(Book).all()
            for book in books:
                if (keyword in book.title) or (keyword in book.author) or (keyword in book.genre):
                    results.append(book.to_dict())
            return results
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
    
    def get_user_preferred_genres(self, user_id: int) -> dict:
        """Get user's preferred genres based on borrowing history."""
        session = get_session()
        try:
            borrowed_books = session.query(Book).join(Borrowing).filter(
                Borrowing.user_id == user_id
            ).all()
            
            if not borrowed_books:
                return {}
            genre_counts = Counter(book.genre for book in borrowed_books)
            total_borrowed = len(borrowed_books)
            genre_preferences = {
                genre: round(count / total_borrowed * 100, 1)
                for genre, count in genre_counts.items()
            }
            
            return genre_preferences
        finally:
            close_session(session)
    
    def recommend_books(self, user_id: int, limit: int = 5) -> list[dict]:
        """Recommend books based on user's borrowing history."""
        session = get_session()
        try:
            # Get user's preferred genres
            genre_preferences = self.get_user_preferred_genres(user_id)
            
            if not genre_preferences:
                # If user has no borrowing history, recommend top-rated books
                books = session.query(Book).order_by(desc(Book.rating)).limit(limit).all()
                result = []
                for book in books:
                    book_dict = book.to_dict()
                    book_dict['recommendation_reason'] = "Top-rated book (no borrowing history)"
                    result.append(book_dict)
                return result
            
            # Get books user has already borrowed (to avoid recommending them again)
            borrowed_book_ids = session.query(Borrowing.book_id).filter(
                Borrowing.user_id == user_id
            ).all()
            borrowed_book_ids = [bid[0] for bid in borrowed_book_ids]
            
            recommended_books = []
            sorted_genres = sorted(genre_preferences.items(), key=lambda x: x[1], reverse=True)
            
            for genre, preference in sorted_genres:
                # Get books from this genre that user hasn't borrowed
                genre_books = session.query(Book).filter(
                    Book.genre == genre,
                    ~Book.id.in_(borrowed_book_ids)
                ).order_by(desc(Book.rating)).limit(limit).all()
                
                recommended_books.extend(genre_books)
                
                if len(recommended_books) >= limit:
                    break
            
            # If we still need more recommendations, add top-rated books from other genres
            if len(recommended_books) < limit:
                remaining_limit = limit - len(recommended_books)
                additional_books = session.query(Book).filter(
                    ~Book.id.in_(borrowed_book_ids + [book.id for book in recommended_books])
                ).order_by(desc(Book.rating)).limit(remaining_limit).all()
                
                recommended_books.extend(additional_books)
            
            # Add recommendation reason to each book
            result = []
            for book in recommended_books[:limit]:
                book_dict = book.to_dict()
                book_genre_preference = genre_preferences.get(book.genre, 0)
                if book_genre_preference > 0:
                    book_dict['recommendation_reason'] = f"You've borrowed {book_genre_preference}% {book.genre} books"
                else:
                    book_dict['recommendation_reason'] = "Top-rated book"
                result.append(book_dict)
            
            return result
        finally:
            close_session(session)
    
    def get_user_reading_profile(self, user_id: int) -> dict:
        """Get comprehensive reading profile for a user."""
        session = get_session()
        try:
            # user info
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return {}
            
            # borrowing statistics
            total_borrowed = session.query(Borrowing).filter(Borrowing.user_id == user_id).count()
            currently_borrowed = session.query(Borrowing).filter(
                Borrowing.user_id == user_id,
                Borrowing.returned_at.is_(None)
            ).count()
            
            # genre preferences
            genre_preferences = self.get_user_preferred_genres(user_id)
            
            # favorite authors
            borrowed_books = session.query(Book).join(Borrowing).filter(
                Borrowing.user_id == user_id
            ).all()
            
            author_counts = Counter(book.author for book in borrowed_books)
            favorite_authors = dict(author_counts.most_common(3))
            
            return {
                'user': user.to_dict(),
                'total_books_borrowed': total_borrowed,
                'currently_borrowed': currently_borrowed,
                'genre_preferences': genre_preferences,
                'favorite_authors': favorite_authors,
                'most_recent_borrowings': [
                    book.to_dict() for book in borrowed_books[-3:]  # Last 3 books
                ]
            }
        finally:
            close_session(session)
