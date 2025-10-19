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

# Create books
create(
    'books.json',
    MAX_BOOK,
    [
        ('title', 'word'),
        ('author', 'name'),
        ('genre', 'word'),
        ('year', 'year'),
        ('rating', 'pyfloat', {'min_value': 0, 'max_value': 10, 'right_digits': 1})
    ]
)

# Create users
create(
    'users.json',
    MAX_USER,
    [
        ('name', 'name'),
    ]
)