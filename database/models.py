from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base, engine

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    age = Column(Integer)
    avatar = Column(String)
    reg_date = Column(DateTime, default=datetime.now())
    birthday_date = Column(DateTime)
    number_of_purchases = Column(Integer, default=0)
    book_fk = relationship('Book', lazy='subquery')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    photo = Column(String, nullable=False)
    genre = Column(String)
    post_date = Column(DateTime, default=datetime.now())
    number_of_pages = Column(String)
    stock = Column(Integer, nullable=False)
    user_fk = relationship(User, lazy='subquery')


def create_tables():
    Base.metadata.create_all(engine)