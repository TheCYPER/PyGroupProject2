"""
Comprehensive timing test for search algorithms.
"""

from db_init import init_db, get_session, close_session
from library import Library
from models.book import Book
from models.user import User
import json
import time
import statistics

def timing_test():
    """Test search performance with different dataset sizes."""
    print("=== Search Algorithm Performance Test ===\n")
    
    # Initialize database
    init_db()
    library = Library()
    
    # Load books from JSON
    with open('books.json', 'r') as f:
        book_set = json.load(f)
    
    session = get_session()
    for book_data in book_set:
        session.add(Book(**book_data))
    session.commit()
    close_session(session)
    
    # Load users from JSON
    with open('users.json', 'r') as f:
        user_set = json.load(f)
    
    session = get_session()
    for user_data in user_set:
        session.add(User(**user_data))
    session.commit()
    close_session(session)
    
    print(f"Loaded {len(book_set)} books and {len(user_set)} users into database.\n")
    
    # Test keywords
    test_keywords = ["Python", "Science", "Fiction", "Technology", "History", "Art", "Music", "Business"]
    
    print("=== Individual Test Results ===")
    naive_times = []
    advanced_times = []
    
    for keyword in test_keywords:
        # Test naive search
        start_time = time.time()
        naive_results = library.naive_search_books(keyword)
        naive_time = time.time() - start_time
        naive_times.append(naive_time)
        
        # Test advanced search
        start_time = time.time()
        advanced_results = library.search_books(keyword)
        advanced_time = time.time() - start_time
        advanced_times.append(advanced_time)
        
        print(f"Keyword: '{keyword}'")
        print(f"  Naive search: {len(naive_results)} results in {naive_time:.4f} seconds")
        print(f"  Advanced search: {len(advanced_results)} results in {advanced_time:.4f} seconds")
        print(f"  Speedup: {naive_time/advanced_time:.2f}x faster\n")
    
    # Calculate statistics
    print("=== Performance Statistics ===")
    print(f"Naive Search:")
    print(f"  Average time: {statistics.mean(naive_times):.4f} seconds")
    print(f"  Min time: {min(naive_times):.4f} seconds")
    print(f"  Max time: {max(naive_times):.4f} seconds")
    print(f"  Standard deviation: {statistics.stdev(naive_times):.4f} seconds")
    
    print(f"\nAdvanced Search:")
    print(f"  Average time: {statistics.mean(advanced_times):.4f} seconds")
    print(f"  Min time: {min(advanced_times):.4f} seconds")
    print(f"  Max time: {max(advanced_times):.4f} seconds")
    print(f"  Standard deviation: {statistics.stdev(advanced_times):.4f} seconds")
    
    # Calculate average speedup
    speedups = [naive_times[i] / advanced_times[i] for i in range(len(naive_times))]
    avg_speedup = statistics.mean(speedups)
    print(f"\nAverage speedup: {avg_speedup:.2f}x")
    print(f"Speedup range: {min(speedups):.2f}x - {max(speedups):.2f}x")
    
    # Test with different dataset sizes
    print(f"\n=== Scalability Test ===")
    
    # Test with subset of data
    test_sizes = [100, 500, 1000]
    keyword = "Science"
    
    for size in test_sizes:
        # Create subset
        session = get_session()
        subset_books = session.query(Book).limit(size).all()
        session.close()
        
        # Test naive search on subset
        start_time = time.time()
        naive_count = 0
        for book in subset_books:
            if keyword in book.title or keyword in book.author or keyword in book.genre:
                naive_count += 1
        naive_time = time.time() - start_time
        
        # Test advanced search on subset
        start_time = time.time()
        advanced_results = library.search_books(keyword)
        advanced_time = time.time() - start_time
        
        print(f"Dataset size: {size}")
        print(f"  Naive search: {naive_count} results in {naive_time:.4f} seconds")
        print(f"  Advanced search: {len(advanced_results)} results in {advanced_time:.4f} seconds")
        print(f"  Speedup: {naive_time/advanced_time:.2f}x faster\n")

if __name__ == "__main__":
    timing_test()
