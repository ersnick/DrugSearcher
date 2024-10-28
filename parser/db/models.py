from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from parser.db.database import Base


class Drug(Base):
    __tablename__ = 'drugs'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    atx_code = Column(String(50), nullable=True)
    influence = Column(Text, nullable=True)
    kinetics = Column(Text, nullable=True)
    indication = Column(Text, nullable=True)
    dosage = Column(Text, nullable=True)
    side_effects = Column(Text, nullable=True)
    contraindications = Column(Text, nullable=True)
    pregnancy_and_lactation = Column(Text, nullable=True)
    hepato = Column(Text, nullable=True)
    renal = Column(Text, nullable=True)
    child_use = Column(Text, nullable=True)
    old_use = Column(Text, nullable=True)
    special_instructions = Column(Text, nullable=True)
    overdose = Column(Text, nullable=True)
    interactions = Column(Text, nullable=True)
    storage_conditions = Column(Text, nullable=True)
    storage_time = Column(Text, nullable=True)
    pharmacy_conditions = Column(Text, nullable=True)

    active_ingredients = relationship("ActiveIngredient", back_populates="drug", cascade="all, delete-orphan")


class ActiveIngredient(Base):
    __tablename__ = 'active_ingredients'

    id = Column(Integer, primary_key=True)
    drug_id = Column(Integer, ForeignKey('drugs.id'), nullable=False)
    name = Column(String(255), nullable=False)
    dosage = Column(String(255), nullable=True)

    drug = relationship("Drug", back_populates="active_ingredients")