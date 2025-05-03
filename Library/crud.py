from .database import get_db_connection
from typing import List, Optional

# Members CRUD operations
def create_member(member_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    INSERT INTO members (first_name, last_name, email, phone, address, membership_date, membership_status)
    VALUES (%s, %s, %s, %s, %s, CURDATE(), 'active')
    """
    cursor.execute(query, (
        member_data['first_name'],
        member_data['last_name'],
        member_data['email'],
        member_data.get('phone'),
        member_data.get('address')
    ))
    member_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return member_id

def get_member(member_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM members WHERE member_id = %s"
    cursor.execute(query, (member_id,))
    member = cursor.fetchone()
    cursor.close()
    conn.close()
    return member

def get_all_members():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM members"
    cursor.execute(query)
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return members

def update_member(member_id: int, member_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE members 
    SET first_name = %s, last_name = %s, email = %s, phone = %s, address = %s, membership_status = %s
    WHERE member_id = %s
    """
    cursor.execute(query, (
        member_data['first_name'],
        member_data['last_name'],
        member_data['email'],
        member_data.get('phone'),
        member_data.get('address'),
        member_data.get('membership_status', 'active'),
        member_id
    ))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    return affected_rows

def delete_member(member_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM members WHERE member_id = %s"
    cursor.execute(query, (member_id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    return affected_rows

# Books CRUD operations
def create_book(book_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    INSERT INTO books (title, isbn, publication_year, publisher_id, category, total_copies, available_copies)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        book_data['title'],
        book_data['isbn'],
        book_data.get('publication_year'),
        book_data.get('publisher_id'),
        book_data.get('category'),
        book_data.get('total_copies', 1),
        book_data.get('available_copies', book_data.get('total_copies', 1))
    ))
    book_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return book_id

def get_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM books WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    return book

def get_all_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM books"
    cursor.execute(query)
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books

def update_book(book_id: int, book_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get current available copies to maintain consistency
    current_book = get_book(book_id)
    if not current_book:
        return 0
    
    # Calculate new available copies if total copies is being updated
    if 'total_copies' in book_data:
        diff = book_data['total_copies'] - current_book['total_copies']
        book_data['available_copies'] = current_book['available_copies'] + diff
    
    query = """
    UPDATE books 
    SET title = %s, isbn = %s, publication_year = %s, publisher_id = %s, 
        category = %s, total_copies = %s, available_copies = %s
    WHERE book_id = %s
    """
    cursor.execute(query, (
        book_data['title'],
        book_data['isbn'],
        book_data.get('publication_year'),
        book_data.get('publisher_id'),
        book_data.get('category'),
        book_data.get('total_copies', current_book['total_copies']),
        book_data.get('available_copies', current_book['available_copies']),
        book_id
    ))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    return affected_rows

def delete_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM books WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    return affected_rows

# Loans CRUD operations
def create_loan(loan_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Check if book is available
    book = get_book(loan_data['book_id'])
    if not book or book['available_copies'] <= 0:
        return None
    
    # Create loan
    query = """
    INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date, status)
    VALUES (%s, %s, %s, %s, NULL, 'active')
    """
    cursor.execute(query, (
        loan_data['book_id'],
        loan_data['member_id'],
        loan_data['loan_date'],
        loan_data['due_date']
    ))
    loan_id = cursor.lastrowid
    
    # Update available copies
    update_query = "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s"
    cursor.execute(update_query, (loan_data['book_id'],))
    
    conn.commit()
    cursor.close()
    conn.close()
    return loan_id

def get_loan(loan_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM loans WHERE loan_id = %s"
    cursor.execute(query, (loan_id,))
    loan = cursor.fetchone()
    cursor.close()
    conn.close()
    return loan

def get_all_loans():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM loans"
    cursor.execute(query)
    loans = cursor.fetchall()
    cursor.close()
    conn.close()
    return loans

def return_loan(loan_id: int, return_date: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get loan details to know which book is being returned
    loan = get_loan(loan_id)
    if not loan:
        return 0
    
    # Update loan
    query = """
    UPDATE loans 
    SET return_date = %s, status = 'returned'
    WHERE loan_id = %s
    """
    cursor.execute(query, (return_date, loan_id))
    
    # Update available copies
    update_query = "UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s"
    cursor.execute(update_query, (loan['book_id'],))
    
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    return affected_rows