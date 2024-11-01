from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.drugs import DrugSchema
from search_module import search_drug

router = APIRouter()


@router.get("/drug/{name}", response_model=DrugSchema)
def get_drug(name: str, db: Session = Depends(get_db)):
    drug = search_drug(db, name=name)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return drug
