"""
Simple test for Smart Library System.
"""

from db_init import init_db, get_session, close_session
from library import Library
from models.book import Book
from models.user import User
import json
import time

def test():
    """Simple test."""
    print("Testing Library System...")
    
    # Initialize database
    init_db()
    
    # Create library
    library = Library()

    # Add book
    with open('books.json', 'r') as f: # Read JSON file
        book_set = json.load(f)

    session = get_session()
    for i in book_set:
        session.add(Book(**i))
    session.commit()
    close_session(session=session)

    # Manually add book
    book = library.add_book("Python Guide", "John Doe", "Programming", 2023, 4.5)
    print(f"Added book: {book['title']}")
    
    # Add user
    with open('users.json', 'r') as f: # Read JSON file
        user_set = json.load(f)

    session = get_session()
    for i in user_set:
        session.add(User(**i))
    session.commit()
    close_session(session=session)

    user = library.add_user("Alice")
    print(f"Added user: {user['name']}")
    
    # Search
    start = time.time()
    results = library.naive_search_books("Python")
    end = time.time()
    print(f"By naive search, found {len(results)} books, using {end - start:.4f} seconds")

    start = time.time()
    results = library.search_books("Python")
    end = time.time()
    print(f"By advanced search, found {len(results)} books, using {end - start:.4f} seconds")
    
    # Borrow
    library.borrow_book(user['id'], book['id'])
    print("Book borrowed")
    
    # Stats
    stats = library.get_statistics()
    print(f"Total books: {stats['total_books']}")
    
    print("Test completed!")

if __name__ == "__main__":
    test()
