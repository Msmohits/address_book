# Address Book API

A minimal **Address Book API** built with **FastAPI** and **SQLite**.  
Users can **create, update, delete, and fetch addresses**, including querying addresses **within a given distance** from a location.  
Token-based authentication is implemented for API security.

---

## Features

- Create, update, delete addresses
- Store coordinates (latitude & longitude) in SQLite
- Retrieve addresses within a given distance
- Token-based authentication
- Auto-create database tables on startup
- Fully documented API using **Swagger UI**

---

## Technologies Used

- Python 3.12
- FastAPI/ FastApi Standard
- SQLAlchemy (ORM)
- Pydantic (schemas & validation)
- SQLite (database)
- Uvicorn (ASGI server)

---

## Setup Instructions

### 1. Clone the repository and setup

```bash
git clone https://github.com/Msmohits/address_book.git
cd address_book
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
OR
fastapi run

```
#### 3. Access the API documentation
Open your browser and navigate to:
http://0.0.0.0:8000/docs

and use auth token: X4M8P2Q9Z7


