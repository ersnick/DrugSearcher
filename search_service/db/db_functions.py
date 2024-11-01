from sqlalchemy.orm import Session, joinedload
from db.models import Drug


def get_drug(db: Session, name: str):
    return db.query(Drug).options(joinedload(Drug.active_ingredients)).filter(Drug.name == name).first()
