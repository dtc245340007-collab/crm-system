import os, logging, datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("crm_app")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://crm_user:SecurePassword123!@db:5432/crm_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM System API")
Instrumentator().instrument(app).expose(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    logger.info("Access CRM home endpoint")
    return {"message": "He thong CRM dang hoat dong", "status": "online"}

@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    logger.info("Fetch customer list")
    return db.query(Customer).all()

@app.post("/customers")
def create_customer(name: str, email: str, phone: str = "", notes: str = "", db: Session = Depends(get_db)):
    customer = Customer(name=name, email=email, phone=phone, notes=notes)
    db.add(customer)
    try:
        db.commit()
        db.refresh(customer)
        logger.info(f"Added new customer: {email}")
        return customer
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating customer: {str(e)}")
        raise HTTPException(status_code=400, detail="Loi du lieu hoac trung email")
