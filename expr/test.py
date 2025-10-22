"""
test
"""

from db_init import init_db, get_session, close_session
from library import Library
from models.book import Book
import json
import time, random, string, timeit
import numpy as np
import pandas as pd

ll = [0, 100, 200, 500, 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7]
N = [int(n) for n in ll]
repetition = 3

def load_data(l, r):
    print(f"Start reading data")
    with open('books.json', 'r') as f:
        book_set = json.load(f)
    print(f"Finish reading data")

    print(f"Start loading data")
    session = get_session()
    for i in book_set[l : r]:
        session.add(Book(**i))
    session.commit()
    close_session(session=session)
    print(f"Finish loading data")

def count_time(func, para):
    start = time.time()
    results = func(*para)
    end = time.time()
    return (results, end - start)

def search(func, objv, echo=True):
    foo = count_time(func, [objv])
    if echo:
        print(f"By {func.__name__}, found {len(foo[0])} books, using {foo[1]:.4f} seconds")
    return foo[0]

def test():
    print("Testing Library System...")
    
    init_db()
    library = Library()

    results_nv, results_ad = [], []
    for i in range(1, len(N)):
        print(f"Running, N = {N[i]}")
        load_data(N[i - 1], N[i])
        tmp_nv, tmp_ad = [], []
        objectives = [
            ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            for _ in range(3)
        ]
        for objv in objectives:
            tmp_nv += timeit.repeat(
                stmt=lambda: search(library.naive_search_books, objv),
                number=1,
                repeat=repetition
            )
            tmp_ad += timeit.repeat(
                stmt=lambda: search(library.search_books, objv),
                number=1,
                repeat=repetition
            )
        
        results_nv.append({
            'value': N[i],
            'mean_time': np.mean(tmp_nv),
            'std_time': np.std(tmp_nv),
            'min_time': np.min(tmp_nv),
            'max_time': np.max(tmp_nv)
        })
        results_ad.append({
            'value': N[i],
            'mean_time': np.mean(tmp_ad),
            'std_time': np.std(tmp_ad),
            'min_time': np.min(tmp_ad),
            'max_time': np.max(tmp_ad)
        })
    df_nv = pd.DataFrame(results_nv)
    df_nv.to_csv('results_nv.csv', index=False)
    df_ad = pd.DataFrame(results_ad)
    df_ad.to_csv('results_ad.csv', index=False)
    
    
    print("Test completed!")

if __name__ == "__main__":
    test()
