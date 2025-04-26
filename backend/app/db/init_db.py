# app/db/init_db.py
from app.db.session import engine
from app.db.base import SQLModel

def init_db():
    print("Initializing database...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database initialized!")