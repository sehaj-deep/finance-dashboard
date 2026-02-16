from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///../data/finance.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    category = Column(String, index=True)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String, default="Expense") # Expense or Income

class CategoryRule(Base):
    __tablename__ = "category_rules"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, index=True)
    category = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Seed default categories
    session = SessionLocal()
    if session.query(Category).count() == 0:
        defaults = [
            "Food", "Transport", "Utilities", "Rent", "Entertainment", 
            "Shopping", "Income", "Investment", "Health", "Other"
        ]
        for name in defaults:
            session.add(Category(name=name))
        session.commit()
    session.close()

def get_db_session():
    return SessionLocal()
