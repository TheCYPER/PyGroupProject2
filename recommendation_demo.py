"""
Comprehensive demonstration of the recommendation system.
"""

from db_init import init_db, get_session, close_session
from library import Library
from models.book import Book
from models.user import User
import json

def demo_recommendation_system():
    """Demonstrate the recommendation system with various scenarios."""
    print("=== Smart Library Recommendation System Demo ===\n")
    
    init_db()
    library = Library()
    
    with open('books.json', 'r') as f:
        book_set = json.load(f)
    
    session = get_session()
    for book_data in book_set:
        session.add(Book(**book_data))
    session.commit()
    close_session(session)
    
    with open('users.json', 'r') as f:
        user_set = json.load(f)
    
    session = get_session()
    for user_data in user_set:
        session.add(User(**user_data))
    session.commit()
    close_session(session)
    
    print(f"Loaded {len(book_set)} books and {len(user_set)} users into database.\n")
    
    print("=== Scenario 1: New User (No Borrowing History) ===")
    new_user = library.add_user("New Reader")
    print(f"Created user: {new_user['name']}")
    
    recommendations = library.recommend_books(new_user['id'], limit=5)
    print(f"\nRecommendations for {new_user['name']}:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec['title']} by {rec['author']}")
        print(f"     Genre: {rec['genre']}, Rating: {rec['rating']}")
        print(f"     Reason: {rec['recommendation_reason']}\n")
    
    print("=== Scenario 2: Programming Enthusiast ===")
    prog_user = library.add_user("Code Master")
    
    session = get_session()
    prog_books = session.query(Book).filter(Book.genre == 'Programming').limit(3).all()
    session.close()
    
    for book in prog_books:
        library.borrow_book(prog_user['id'], book.id)
        print(f"Borrowed: {book.title} by {book.author} ({book.genre})")
    
    recommendations = library.recommend_books(prog_user['id'], limit=5)
    print(f"\nRecommendations for {prog_user['name']}:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec['title']} by {rec['author']}")
        print(f"     Genre: {rec['genre']}, Rating: {rec['rating']}")
        print(f"     Reason: {rec['recommendation_reason']}\n")
    
    profile = library.get_user_reading_profile(prog_user['id'])
    print(f"Reading Profile for {prog_user['name']}:")
    print(f"  Total books borrowed: {profile['total_books_borrowed']}")
    print(f"  Currently borrowed: {profile['currently_borrowed']}")
    print(f"  Genre preferences: {profile['genre_preferences']}")
    print(f"  Favorite authors: {profile['favorite_authors']}\n")
    
    print("=== Scenario 3: Diverse Reader ===")
    diverse_user = library.add_user("Book Worm")
    
    session = get_session()
    fiction_books = session.query(Book).filter(Book.genre == 'Fiction').limit(2).all()
    sci_fi_books = session.query(Book).filter(Book.genre == 'Science Fiction').limit(2).all()
    mystery_books = session.query(Book).filter(Book.genre == 'Mystery').limit(1).all()
    session.close()
    
    all_borrowed = fiction_books + sci_fi_books + mystery_books
    for book in all_borrowed:
        library.borrow_book(diverse_user['id'], book.id)
        print(f"Borrowed: {book.title} by {book.author} ({book.genre})")
    
    recommendations = library.recommend_books(diverse_user['id'], limit=5)
    print(f"\nRecommendations for {diverse_user['name']}:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec['title']} by {rec['author']}")
        print(f"     Genre: {rec['genre']}, Rating: {rec['rating']}")
        print(f"     Reason: {rec['recommendation_reason']}\n")
    
    profile = library.get_user_reading_profile(diverse_user['id'])
    print(f"Reading Profile for {diverse_user['name']}:")
    print(f"  Total books borrowed: {profile['total_books_borrowed']}")
    print(f"  Currently borrowed: {profile['currently_borrowed']}")
    print(f"  Genre preferences: {profile['genre_preferences']}")
    print(f"  Favorite authors: {profile['favorite_authors']}\n")
    
    print("=== Scenario 4: Database Genre Analysis ===")
    session = get_session()
    from sqlalchemy import func
    genre_stats = session.query(Book.genre, func.count(Book.id)).group_by(Book.genre).order_by(func.count(Book.id).desc()).all()
    session.close()
    
    print("Top genres in database:")
    for genre, count in genre_stats[:10]:
        print(f"  {genre}: {count} books")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo_recommendation_system()
