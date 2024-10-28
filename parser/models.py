from sqlalchemy import Column, Integer, String, Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session, relationship

load_dotenv()

# строка подключения к базе данных PostgreSQL
database_url = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Создание объекта Engine для подключения
engine = create_engine(database_url)

# Создание сессии
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


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
