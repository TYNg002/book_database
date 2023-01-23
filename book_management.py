##### Libraries #####

import sqlite3
from tabulate import tabulate

##### Functions #####

def int_check(question):
    while True:
        try:
            item = int(input(question))
            break
        except ValueError:
            print("Please enter an integer.")
    return item

# get id of existing book; keep asking for id until valid id is given
def get_id():
    selected_book = None
    # ask for book id
    book_id = int_check('\nEnter the id of the book:\n')
    cursor.execute('''SELECT * FROM books WHERE id = ?''', (book_id, ))
    selected_book = cursor.fetchone()    
    # print error message and ask for id again if id not in database
    while selected_book == None:
        print('''id not recognised. Please try again.''')
        book_id = int_check('\nEnter the id of the book:\n')
        cursor.execute('''SELECT * FROM books WHERE id = ?''', (book_id, ))
        selected_book = cursor.fetchone()
    return book_id

# enter a new book into the database
def enter_book():
    while True:
        try:
            new_id = int_check('\nEnter the id of the new book:\n')
            # check if id already exists and if yes, ask for different id
            cursor.execute('''SELECT * FROM books WHERE id = ?''', (new_id, ))
            id_check = cursor.fetchall()
            while id_check != []:
                print("That id is already taken. Please try a different id.")
                new_id = int_check('Enter the id of the new book:\n')
                cursor.execute('''SELECT * FROM books WHERE id = ?''', (new_id, ))
                id_check = cursor.fetchall()
            new_title = input('Enter the title of the new book:\n')
            new_author = input('Enter the author of the new book:\n')
            new_qty = int_check('Enter a quantity for the new book:\n')
            cursor.execute('''
                INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''', 
                (new_id, new_title, new_author, new_qty))
            print(f'{new_qty} of the new book titled {new_title} (id {new_id}) '
                  f'written by {new_author} has been added.\n')
            db.commit()
            break
        except ValueError:
            print('Enter an integer for id and quantity. Please try again.\n')

# update information on a book
def update_book():
    book_id = get_id()
    # present menu for update type
    update_type = ''
    while update_type != ('1' and '2' and '3'):
        update_type = input('''\nWhich information would you like to update:
1. Title
2. Author
3. Quantity
Chosen option: ''')
        if update_type == '1':
            title = input('Enter the desired book title: ')
            cursor.execute('''UPDATE books SET Title = ? WHERE id = ? ''', 
                (title, book_id)
            )
            print(f'\nTitle updated to: {title}')
        elif update_type == '2':
            author = input('Enter the desired book author: ')
            cursor.execute('''UPDATE books SET Author = ? WHERE id = ? ''', 
                (author, book_id)
            )
            print(f'\nAuthor updated to: {author}')
        elif update_type == '3':
            qty = input('Enter the desired book quantity: ')
            cursor.execute('''UPDATE books SET Qty = ? WHERE id = ? ''', 
                (qty, book_id)
            )
            print(f'\nQuantity updated to: {qty}')
        else:
            print('Ensure you have entered an integer which correlates to the '
                  'menu options.''')

    db.commit()

# delete information on a book
def delete_book():
    book_id = get_id()
    print(f'\nData of book id {book_id} deleted!')
    cursor.execute('''DELETE FROM books WHERE id = ? ''', (book_id,))

    db.commit()

# view information on a book
def search_book():
    # present menu for search type
    search_type = ''
    while search_type != ('1' and '2' and '3'):
        search_type = input('''Search by:
1. id
2. Title
3. Author
Chosen option: ''')
        # print search results based on chosen search type
        if search_type == '1':
            book_id = input('Enter the book id: ')
            cursor.execute('''\nSELECT * FROM books WHERE id = ?''', (book_id, ))
            selected_book = cursor.fetchall()
            print(tabulate(selected_book, headers))
        elif search_type == '2':
            title = '%' + input('Enter the book title: ') + '%'
            cursor.execute('''SELECT * FROM books WHERE Title LIKE ?''', (title, ))
            selected_book = cursor.fetchall()
            print(tabulate(selected_book, headers))
        elif search_type == '3':
            author = '%' + input('Enter the book author: ') + '%'
            cursor.execute('''SELECT * FROM books WHERE Author LIKE ?''', (author, ))
            selected_book = cursor.fetchall()
            print(tabulate(selected_book, headers))
        else:
            print('''Ensure you have entered an integer which correlates to the 
menu options.''')

    db.commit()

# view all books in database
def view_all():
    cursor.execute('''SELECT * FROM books''')
    all_books = cursor.fetchall()
    print("")
    print(tabulate(all_books, headers))

##### Initial program setup #####

# create books_db file
db = sqlite3.connect('books_db')

# Get a cursor object
cursor = db.cursor()  

# create and populate a table called 'books'
# if the table already exists, skip the 'try' block
try:
    # create table named 'books' with id, Title, Author, and Qty columns
    cursor.execute('''
        CREATE TABLE books(id INTEGER PRIMARY KEY, Title TEXT,
        Author TEXT, Qty INTEGER)
''')
    db.commit()
    # populate 'books' with rows
    books_info = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling ', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis ', 25),
        (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll ', 12)
    ]
    cursor.executemany('''
        INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''', 
        books_info)
    db.commit()
except sqlite3.OperationalError:
    pass

# set headers for tabulated results
headers = ["id", "Title", "Author", "Qty"]

##### Menu section #####

print('Welcome to the book management program.')

menu = ''

# present menu options
while menu != '0':
    menu = input('''\nPlease select one of the following options:
1. Enter book
2. Update book
3. Delete book
4. Search books
5. View all books
0. Exit
Chosen option: ''')
    if menu == '1':
        enter_book()
    elif menu == '2':
        update_book()
    elif menu == '3':
        delete_book()
    elif menu == '4':
        search_book()
    elif menu == '5':
        view_all()
    elif menu == '0':
        print('The program will now terminate.')
        db.close()
        exit
    else:
        print('\nEnsure you have entered an integer which correlates to the '
              'menu options.')