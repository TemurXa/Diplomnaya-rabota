from fastapi import FastAPI
from api.users import user_router
from api.books import book_router

app = FastAPI()

app.include_router(user_router)
app.include_router(book_router)