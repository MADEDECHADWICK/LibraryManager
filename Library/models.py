from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    member_id: int
    membership_date: date
    membership_status: str

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    isbn: str = Field(..., min_length=10, max_length=20)
    publication_year: Optional[int] = None
    category: Optional[str] = None
    total_copies: int = 1

class BookCreate(BookBase):
    pass

class Book(BookBase):
    book_id: int
    available_copies: int

    class Config:
        from_attributes = True

class LoanBase(BaseModel):
    book_id: int
    member_id: int
    loan_date: date
    due_date: date

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    loan_id: int
    return_date: Optional[date] = None
    status: str

    class Config:
        from_attributes = True