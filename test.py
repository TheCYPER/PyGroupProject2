"""
Simple test for Smart Library System.
"""

from db_init import init_db
from library import Library

def test():
    """Simple test."""
    print("Testing Library System...")
    
    # Initialize database
    init_db()
    
    # Create library
    library = Library()
    
    # Add book
    book = library.add_book("Python Guide", "John Doe", "Programming", 2023, 4.5)
    print(f"Added book: {book['title']}")
    
    # Add user
    user = library.add_user("Alice")
    print(f"Added user: {user['name']}")
    
    # Search
    results = library.search_books("Python")
    print(f"Found {len(results)} books")
    
    # Borrow
    library.borrow_book(user['id'], book['id'])
    print("Book borrowed")
    
    # Stats
    stats = library.get_statistics()
    print(f"Total books: {stats['total_books']}")
    
    print("Test completed!")

if __name__ == "__main__":
    test()
