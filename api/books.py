from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from CRUD import User,Book
from sqlalchemy.orm import Session
from database import get_db
from database.bookservice import (add_book_db, get_book_by_id_db, update_book_photo_db, update_book_stock_db)
import os
import shutil

book_router = APIRouter(prefix='/books', tags=['Books'])
AVATAR_DIR = 'media'

@book_router.post('/register')
def register_book(book: Book, db: Session = Depends(get_db)):
    try:
        book_id = add_book_db(db, book.name, book.price, book.photo, book.genre, book.number_of_pages, book.stock)
        return {'message': 'Книга добавлена',
                'book_id': book_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Книга не добавлена\n{e}')

@book_router.get('/profile/{book_id}')
def get_book_profile(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id_db(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail='Книга не найдена')

    return {
        'id': book_id,
        'name': book.name,
        'price': book.price,
        'genre': book.genre,
        'number_of_pages': book.number_of_pages,
        'stock': book.stock
    }

@book_router.post('/photo/upload/{book_id}')
def upload_photo(book_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        os.makedirs(AVATAR_DIR, exist_ok=True)

        file_ext = file.filename.split('.')[-1]
        file_name = f'book_{book_id}_photo.{file_ext}'
        file_path = os.path.join(AVATAR_DIR, file_name)

        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        update_book_photo_db(db, book_id, file_path)
        return {'message': 'Фото обновлено',
                'path': file_path}
    except Exception as e:
        return HTTPException(status_code=500, detail=f'Обновление провалено {e}')


@book_router.post('/stock/upload/{book_id}')
def upload_stock(book_id: int, new_stock: int,  db: Session = Depends(get_db)):
    try:
        update_book_stock_db(db, book_id, new_stock)
        return {'message': 'Количество обновлено',
                'stock': new_stock}
    except Exception as e:
        return HTTPException(status_code=500, detail=f'Обвновление провалено {e}')
