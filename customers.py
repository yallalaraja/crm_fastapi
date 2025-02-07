from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Customer  # Make sure the Customer model is correctly imported
from auth import get_current_user  # Ensure this is imported correctly
from config import SessionLocal
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/customers", tags=["Customers"])

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schema for creating a new customer
class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str

# Pydantic Schema for responding with customer data
class CustomerOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        orm_mode = True  # Allows the response to work directly with SQLAlchemy models

# Create a new customer
@router.post("/", response_model=CustomerOut)
def create_customer(
    customer: CustomerCreate, 
    db: Session = Depends(get_db), 
    user: str = Depends(get_current_user)  # Get the current user
):
    # Create a new customer instance
    new_customer = Customer(name=customer.name, email=customer.email, phone=customer.phone)
    
    # Add the customer to the database and commit
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    # Return the new customer data
    return new_customer

# Get all customers
@router.get("/", response_model=List[CustomerOut])  # List of customers will be returned
def get_customers(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    # Query all customers from the database
    customers = db.query(Customer).all()
    
    # Return the list of customers
    return customers
