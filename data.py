from faker import Faker

MAX_BOOK = 1000 # maximum amount of books
MAX_USER = 10 # maximum amount of users
f = Faker(['en-US'])

def create(f_name, N, content):
    """
    Use faker lib to generate data and write into a json file
    """
    x = f.json(
        data_columns=content,
        num_rows=N
        )

    with open(f_name, 'w') as file:
        file.write(x)

# Create books with realistic genres
def create_realistic_books(f_name, N):
    """Create books with realistic genres."""
    genres = [
        'Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Romance',
        'Thriller', 'Biography', 'History', 'Science', 'Technology', 'Programming',
        'Philosophy', 'Psychology', 'Art', 'Music', 'Travel', 'Cooking', 'Health',
        'Business', 'Economics', 'Politics', 'Education', 'Religion', 'Sports'
    ]
    
    books = []
    for _ in range(N):
        book = {
            'title': f.word(),
            'author': f.name(),
            'genre': f.random_element(elements=genres),
            'year': f.year(),
            'rating': round(f.pyfloat(min_value=1, max_value=5, right_digits=1), 1)
        }
        books.append(book)
    
    import json
    with open(f_name, 'w') as file:
        json.dump(books, file, indent=2)

# Create books with realistic genres
create_realistic_books('books.json', MAX_BOOK)

# Create users
create(
    'users.json',
    MAX_USER,
    [
        ('name', 'name'),
    ]
)