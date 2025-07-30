from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from CRUD import User,Book
from sqlalchemy.orm import Session
from database import get_db
from database.userservice import (create_user_db, get_user_by_id_db, update_user_avatar_db, buy_book_db)
import os
import shutil

user_router = APIRouter(prefix='/users', tags=['Users'])
AVATAR_DIR = 'media'

@user_router.post('/register')
def register_user(user: User, db: Session = Depends(get_db)):
    try:
        user_id = create_user_db(db, user.name, user.phone, user.password, user.age, user.avatar, user.birthday_date)
        return {'message': 'Пользователь создан',
                'user_id': user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Пользователь не создан\n{e}')



@user_router.get('/profile/{user_id}')
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id_db(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    return {
        'id': user_id,
        'name': user.name,
        'phone': user.phone,
        'reg_date': user.reg_date,
        'password': user.password,
        'age': user.age,
        'birthday': user.birthday_date,
        'number_of purchases': user.number_of_purchases
    }

@user_router.post('/avatar/upload/{user_id}')
def upload_avatar(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        os.makedirs(AVATAR_DIR, exist_ok=True)

        file_ext = file.filename.split('.')[-1]
        file_name = f'user_{user_id}_avatar.{file_ext}'
        file_path = os.path.join(AVATAR_DIR, file_name)

        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        update_user_avatar_db(db, user_id, file_path)
        return {'message': 'Аватар обновлен',
                'path': file_path}
    except Exception as e:
        return HTTPException(status_code=500, detail=f'Обновление провалено {e}')

@user_router.post('/buy_book/{user_id}/{book_id}')
def buy_book(user_id: int, book_id: int, db: Session = Depends(get_db)):
    try:
        buy_book_db(db, user_id, book_id)
        return {'message': 'Книга была куплена',
                'book_id': book_id}
    except Exception as e:
        return HTTPException(status_code=500, detail=f'Покупка провалена {e}')

