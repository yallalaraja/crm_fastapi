from sqlalchemy.orm import Session
from config import SessionLocal
from models import Customer

# Create a database session
db: Session = SessionLocal()

# Sample customers to insert
customers = [
    {"name": "John Doe", "email": "john@example.com", "phone": "1234567890"},
    {"name": "Jane Smith", "email": "jane@example.com", "phone": "9876543210"},
]

for customer in customers:
    new_customer = Customer(name=customer["name"], email=customer["email"], phone=customer["phone"])
    db.add(new_customer)

db.commit()
print("Customers inserted successfully!")

# Close the session
db.close()
