from fastapi import APIRouter
from search_module import search_drug

router = APIRouter()


@router.get("/drug/{name}")
def get_drug(name: str):
    pass
