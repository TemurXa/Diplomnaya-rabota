from sqlalchemy.orm import Session
from database.models import User, Book
from datetime import datetime

def create_user_db(db: Session, name: str, phone: str, password: str, age: int, avatar: str, birthday_date: datetime):
    user = db.query(User).filter(User.name == name, User.phone == phone).first()
    if user:
        return user.id
    new_user = User(name=name, phone=phone, password=password, age=age, avatar=avatar, birthday_date=birthday_date)
    db.add(new_user)
    db.commit()
    return  new_user.id

def get_user_by_id_db(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user_avatar_db(db: Session,user_id: int, file_path: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.avatar = file_path
        db.commit()
        return True
    return False

def buy_book_db(db: Session, user_id: int, book_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            if book.stock != 0:
                book.stock = book.stock - 1
                user.number_of_purchases = user.number_of_purchases + 1
                db.commit()
                return True
            return False
        return False
    return False
