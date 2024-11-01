import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends
from api import router
from db.database import get_db
from search_module import search_drug

app = FastAPI()

# Подключение маршрутов
app.include_router(router, prefix="/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
