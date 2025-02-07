# 🚀 CRM Application using FastAPI

This is a **Customer Relationship Management (CRM) API** built with **FastAPI**, using **PostgreSQL** as the database and **JWT authentication** for secure user login.

## 📁 Project Structure
```
crm_fastapi/
│── __pycache__/
│── auth.py               # Handles JWT authentication & password hashing
│── config.py             # Configuration settings (DB connection, environment variables)
│── customers.py          # CRUD operations for managing customers
│── insert_customers.py   # Script to insert dummy customer data
│── insert_users.py       # Script to insert dummy users
│── main.py               # FastAPI entry point
│── models.py             # SQLAlchemy models for database tables
│── requirements.txt      # Dependencies required for the project
│── schemas.py            # Pydantic schemas for request validation
│── .gitignore            # Ignore files in version control
```

---

## 🛠️ **Setup & Installation**
### 1️⃣ **Clone the repository**
```bash
git clone https://github.com/yallalaraja/crm_fastapi.git
cd crm_fastapi
```

### 2️⃣ **Create a virtual environment**
```bash
python -m venv myenv
source myenv/bin/activate  # For Mac/Linux
myenv\Scripts\activate     # For Windows
```

### 3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Set up the PostgreSQL database**
Modify `config.py` to match your **PostgreSQL** connection details:
```python
DATABASE_URL = "postgresql://username:password@localhost:5432/crm_db"
```

### 5️⃣ **Run the database migrations**
```bash
alembic upgrade head
```

### 6️⃣ **Start the FastAPI server**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔑 **Authentication (JWT)**
- **User Registration**: `/register/`
- **User Login & Token Generation**: `/login/`
- **Protected Route Example**: `/protected/`

To access **protected routes**, pass the JWT token as a `Bearer` token in the headers.

---

## 📌 **API Endpoints**
### 🔹 User Authentication
| Method | Endpoint       | Description            |
|--------|--------------|------------------------|
| `POST` | `/register/` | Register a new user    |
| `POST` | `/login/`    | Login & get JWT token  |

### 🔹 Customer Management
| Method | Endpoint      | Description             |
|--------|--------------|-------------------------|
| `POST` | `/customers/register` | Add a new customer      |
| `GET`  | `/protected/` | Retrieve all customers |

---

## 🛠 **Testing with Postman**
1. **Register a user**
   - **Endpoint:** `POST /register/`
   - **Body:**
     ```json
     {
       "username": "admin",
       "password": "securepassword"
     }
     ```
   
2. **Login to get JWT Token**
   - **Endpoint:** `POST /login/`
   - **Body:**
     ```json
     {
       "username": "admin",
       "password": "securepassword"
     }
     ```
   - **Response:**
     ```json
     {
       "access_token": "your_jwt_token",
       "token_type": "bearer"
     }
     ```

3. **Access a protected route**
   - **Endpoint:** `GET /customers/`
   - **Headers:**
     ```
     Authorization: Bearer your_jwt_token
     ```

---

## 🚀 **Future Enhancements**
- ✅ Add pagination for customer listing
- ✅ Implement role-based access control (RBAC)
- ✅ Add more detailed logging & monitoring

---

## 👨‍💻 **Contributing**
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit your changes (`git commit -m "Added new feature"`)
4. Push to your branch (`git push origin feature-branch`)
5. Open a Pull Request

---

## 📜 **License**
This project is licensed under the **MIT License**.

---

### 🌟 **Like this project? Give it a star ⭐ on GitHub!**

