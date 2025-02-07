from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from config import SessionLocal, engine, Base
from models import User
from auth import hash_password, verify_password
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Secret Key & Algorithm for JWT
SECRET_KEY = "your_secret_key"  # Change this to a strong key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

#  Generate JWT Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#  Decode & Verify JWT Token
def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str

@app.post("/customers/register/")
def register_customer(
    customer: CustomerCreate, 
    authorization: str = Header(None), 
    db: Session = Depends(get_db)
):
    """Register a new customer. Requires a valid JWT token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.split(" ")[1]  # Extract token after "Bearer"
    username = get_current_user(token)  # Validate token and get username

    # Check if email or phone already exists
    existing_customer = db.query(Customer).filter(
        (Customer.email == customer.email) | (Customer.phone == customer.phone)
    ).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer with this email or phone already exists")

    # Create and save the new customer
    db_customer = Customer(name=customer.name, email=customer.email, phone=customer.phone)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return {"message": f"Customer {customer.name} registered successfully!", "customer": db_customer}

@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pwd = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User registered successfully"}

@app.post("/login/")
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    """Login user & generate JWT token."""
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

from models import Customer  # Import the Customer model

@app.get("/protected/")
def protected_route(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Protected route that returns a list of customers."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.split(" ")[1]  # Extract token after "Bearer"
    username = get_current_user(token)  # Validate token and get username

    # Fetch all customers from the database
    customers = db.query(Customer).all()

    return {"message": f"Hello, {username}! Here is the customer list:", "customers": customers}
