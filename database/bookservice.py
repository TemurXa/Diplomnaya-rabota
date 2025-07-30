from sqlalchemy.orm import Session
from database.models import User, Book
from datetime import datetime

def add_book_db(db:Session, name:str, price:float, photo:str, genre:str, number_of_pages: int, stock: int):
    book = db.query(Book).filter(Book.name == name).first()
    if book:
        return book.id
    new_book = Book(name=name, price=price, photo=photo, genre=genre, number_of_pages=number_of_pages, stock=stock)
    db.add(new_book)
    db.commit()
    return new_book.id

def get_book_by_id_db(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book_photo_db(db: Session,book_id: int, file_path: str):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.photo = file_path
        db.commit()
        return True
    return False

def update_book_stock_db(db: Session, book_id: int, stock: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.stock = stock
        db.commit()
        return True
    return False