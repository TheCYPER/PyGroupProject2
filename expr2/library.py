"""
Simplified library class for experiment
"""

from db_init import get_session, close_session
from models.book import Book

class Library:
    """Simple library interface."""
    
    def __init__(self):
        self.name = "Smart Library System"
    
    def naive_search_books(self, keyword: str) -> list[dict]:
        """linear search using for loop"""
        session = get_session()
        try:
            results = []
            books = session.query(Book).all()
            for book in books:
                if keyword in book.title:
                    results.append(book.to_dict())
            return results
        finally:
            close_session(session)

    def search_books(self, keyword: str) -> list[dict]:
        """Search books by keyword."""
        session = get_session()
        try:
            books = session.query(Book).filter(
                Book.title.contains(keyword)
            ).all()
            return [book.to_dict() for book in books]
        finally:
            close_session(session)
    