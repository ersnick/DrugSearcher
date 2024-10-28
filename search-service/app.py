from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from logging import INFO


# Настройка логирования
def __config_logger():
    file_log = logging.FileHandler('parser-api.log')
    console_log = logging.StreamHandler()
    FORMAT = '[%(levelname)s] %(asctime)s : %(message)s | %(filename)s'
    logging.basicConfig(level=INFO,
                        format=FORMAT,
                        handlers=(file_log, console_log),
                        datefmt='%d-%m-%y - %H:%M:%S')


logger = logging.getLogger()
__config_logger()


# Обработчик события запуска приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    pass

app = FastAPI(lifespan=lifespan)
