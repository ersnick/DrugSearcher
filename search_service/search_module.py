from db.db_functions import get_drug
from sqlalchemy.orm import Session, joinedload

from db.models import Drug


def search_drug(db: Session, name: str):
    return get_drug(db, name)
