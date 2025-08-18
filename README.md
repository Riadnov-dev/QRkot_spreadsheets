# 📊 QRKot Spreadsheets — FastAPI + Google Sheets
Backend for managing charity projects and donations with automatic investing and Google Sheets reports.
Create projects with target amounts, accept donations that are auto-allocated to open projects, and generate a shareable spreadsheet via a Google service account.

## 🧰 Tech Stack
[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/) 
[![FastAPI](https://img.shields.io/badge/FastAPI-0.9x-009688?logo=fastapi)](https://fastapi.tiangolo.com/) 
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-8A2BE2?logo=python)](https://www.sqlalchemy.org/) 
[![Alembic](https://img.shields.io/badge/Alembic-DB%20migrations-4B8BBE?logo=python)](https://alembic.sqlalchemy.org/) 
[![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?logo=pydantic)](https://docs.pydantic.dev/) 
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-3949AB?logo=python)](https://www.uvicorn.org/) 
[![SQLite](https://img.shields.io/badge/SQLite-DB-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/) 
[![Google%20Sheets%20API](https://img.shields.io/badge/Google%20Sheets%20API-Reports-34A853?logo=googlesheets&logoColor=white)](https://developers.google.com/sheets) 
[![Google%20Drive%20API](https://img.shields.io/badge/Google%20Drive%20API-Sharing-4285F4?logo=googledrive&logoColor=white)](https://developers.google.com/drive) 
[![Pytest](https://img.shields.io/badge/Pytest-Tests-0A9EDC?logo=pytest)](https://docs.pytest.org/) 
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-6BA539?logo=openapiinitiative&logoColor=white)](https://www.openapis.org/)



## ✨ Features
🏗 Projects & Donations — create projects (name, description, goal); donations are automatically invested into open projects until targets are reached.

📈 Google Sheets reports — create a spreadsheet with top projects by completion speed and grant user access via Google Drive.

👤 Auth & roles — registration/authentication; superuser-only protected operations.

🛡 Clean architecture — Pydantic schemas, SQLAlchemy models, CRUD layer, validation, service layer (investment + Google API).

🔄 Migrations & tests — Alembic baseline; comprehensive pytest suite with fixtures.

📜 Interactive API docs — OpenAPI available at /docs and /redoc.

### 🚀 Quick Start
Clone the repository:

```
git clone https://github.com/Riadnov-dev/QRKot_spreadsheets.git

cd QRKot_spreadsheets
```

Create and activate a virtual environment:

```
python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Create a .env file (see examples below), then run migrations:

```
alembic upgrade head
```

Start the application:

```
uvicorn app.main:app --reload
```

Open the docs in a browser:
```

Swagger UI → http://127.0.0.1:8000/docs

Redoc → http://127.0.0.1:8000/redoc
```

### 🔐 Environment Variables

Minimal configuration:

```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db

SECRET=your_secret_key
```

Google service account (enable Google Sheets API and Google Drive API in Google Cloud; create a service account and copy JSON fields):

```
EMAIL=your.personal@gmail.com          # user to grant access to the report
TYPE=service_account
PROJECT_ID=...
PRIVATE_KEY_ID=...
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=...@...iam.gserviceaccount.com
CLIENT_ID=...
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=...
```
Keep PRIVATE_KEY exactly as a quoted one-line string with literal \n breaks.

### 📌 API Endpoints (overview)
Projects
```
GET     /projects/          # List all projects
POST    /projects/          # Create a project (superuser only)
PATCH   /projects/{id}      # Update a project (superuser only)
DELETE  /projects/{id}      # Delete a project (superuser only)
```

Donations
```
GET     /donations/         # List all donations (superuser only)
POST    /donations/         # Create a donation (authenticated)
GET     /donations/my       # List current user's donations (authenticated)
```
Reports
```
GET     /reports/           # Generate Google Sheets report (superuser only
```
Auth & Users
```
POST    /auth/jwt/login     # Authenticate a user
POST    /auth/register      # Register a new user
GET     /users/             # List users (superuser only)
PATCH   /users/{id}         # Update user (superuser only)
# User deletion is disabled
```

### 🧠 How investing works (core logic)
Donations and projects both track full_amount (goal) and invested_amount.

The service iterates through open counterparts and distributes funds:

When an entity reaches its goal, it’s marked fully_invested and timestamped with close_date.

Distribution stops when either the incoming donation or the target project is fully funded.

This logic is implemented in the service layer (services/investment.py), keeping endpoints slim and testable.

### 📈 Google Sheets report
Spreadsheet title: “Report as of {date}”

Sheet layout includes:

“Report date” with current timestamp

“Top projects by completion speed”

A table with Project name, Duration, Description

The report is created via Sheets API and access is granted via Drive API to the email in .env (EMAIL).

### 🧪 Tests
Run the test suite:
```
pytest
```

Key tests (examples):


tests/test_auth.py, tests/test_credentials.py

tests/test_charity_project.py, tests/test_donations.py, tests/test_investment.py

tests/test_db.py, tests/test_google_auth.py

tests/fixtures/ — reusable data & helpers

### 🗄️ Database & Migrations
Apply the latest migrations:

```
alembic upgrade head
```

Create a new migration after model changes:
```
alembic revision -m "your message"

alembic upgrade head
```

### 📂 Project Structure
```
QRKot_spreadsheets/
├─ alembic/
│  ├─ versions/
│  │  └─ 05e885e53847_first_migration.py
│  ├─ env.py
│  └─ script.py.mako
├─ app/
│  ├─ api/
│  │  ├─ endpoints/            # charity_project.py, donation.py, google_api.py, user.py
│  │  ├─ routers.py
│  │  └─ validators.py
│  ├─ core/                    # base, config, db, google_client, init_db, user
│  ├─ crud/                    # base, charity_project, donation
│  ├─ models/                  # charity_project, donation, user
│  ├─ schemas/                 # pydantic schemas
│  ├─ services/                # investment.py, google_api.py
│  └─ main.py                  # FastAPI app
├─ tests/
│  ├─ fixtures/
│  ├─ test_auth.py
│  ├─ test_charity_project.py
│  ├─ test_credentials.py
│  ├─ test_db.py
│  ├─ test_donations.py
│  ├─ test_google_auth.py
│  └─ test_investment.py
├─ openapi.json
├─ requirements.txt
├─ pytest.ini
├─ fastapi.db / test.db
└─ README.md
```

### 👤 Author

Nikita Riadnov

GitHub Profile: https://github.com/Riadnov-dev

