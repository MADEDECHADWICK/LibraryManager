from fastapi import FastAPI, HTTPException
from .database import get_db_connection
from .models import Member, MemberCreate, Book, BookCreate, Loan, LoanCreate
from .crud import (
    create_member, get_member, get_all_members, update_member, delete_member,
    create_book, get_book, get_all_books, update_book, delete_book,
    create_loan, get_loan, get_all_loans, return_loan
)
from typing import List

app = FastAPI(title="Library Management API", 
              description="A CRUD API for managing a library system", 
              version="1.0.0")

# Members endpoints
@app.post("/members/", response_model=Member)
def add_member(member: MemberCreate):
    member_id = create_member(member.model_dump())
    if member_id:
        return {**member.model_dump(), "member_id": member_id, "membership_date": "2023-01-01", "membership_status": "active"}
    raise HTTPException(status_code=400, detail="Member creation failed")

@app.get("/members/{member_id}", response_model=Member)
def read_member(member_id: int):
    member = get_member(member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.get("/members/", response_model=List[Member])
def read_all_members():
    return get_all_members()

@app.put("/members/{member_id}", response_model=Member)
def update_member_endpoint(member_id: int, member: MemberCreate):
    updated = update_member(member_id, member.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Member not found")
    return {**member.model_dump(), "member_id": member_id}

@app.delete("/members/{member_id}")
def remove_member(member_id: int):
    deleted = delete_member(member_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted successfully"}

# Books endpoints
@app.post("/books/", response_model=Book)
def add_book(book: BookCreate):
    book_id = create_book(book.model_dump())
    if book_id:
        return {**book.model_dump(), "book_id": book_id, "available_copies": book.total_copies}
    raise HTTPException(status_code=400, detail="Book creation failed")

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    book = get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books/", response_model=List[Book])
def read_all_books():
    return get_all_books()

@app.put("/books/{book_id}", response_model=Book)
def update_book_endpoint(book_id: int, book: BookCreate):
    updated = update_book(book_id, book.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return {**book.model_dump(), "book_id": book_id}

@app.delete("/books/{book_id}")
def remove_book(book_id: int):
    deleted = delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

# Loans endpoints
@app.post("/loans/", response_model=Loan)
def add_loan(loan: LoanCreate):
    loan_id = create_loan(loan.model_dump())
    if not loan_id:
        raise HTTPException(status_code=400, detail="Book not available for loan")
    return {**loan.model_dump(), "loan_id": loan_id, "return_date": None, "status": "active"}

@app.get("/loans/{loan_id}", response_model=Loan)
def read_loan(loan_id: int):
    loan = get_loan(loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@app.get("/loans/", response_model=List[Loan])
def read_all_loans():
    return get_all_loans()

@app.post("/loans/{loan_id}/return")
def return_loan_endpoint(loan_id: int, return_date: str):
    returned = return_loan(loan_id, return_date)
    if not returned:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"message": "Book returned successfully"}