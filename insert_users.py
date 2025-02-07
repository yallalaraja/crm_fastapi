from sqlalchemy.orm import Session
from config import SessionLocal
from models import User
from auth import hash_password

# Create a database session
db: Session = SessionLocal()

# Sample users to insert
users = [
    {"username": "admin2", "password": "admin123"},
    {"username": "user2", "password": "userpass"},
]

for user in users:
    hashed_pwd = hash_password(user["password"])
    new_user = User(username=user["username"], hashed_password=hashed_pwd)
    db.add(new_user)

db.commit()
print("Users inserted successfully!")

# Close the session
db.close()
