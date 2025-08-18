# 📊 QRKot Spreadsheets — FastAPI + Google Sheets  

A **backend service** for managing **charity projects** and **donations** with automatic fund distribution and Google Sheets integration.  
Users can create projects with target amounts, donate to the fund, and generate **shareable spreadsheets** with project statistics using a Google service account.  

---

## 📌 About the Project  

**QRKot Spreadsheets** was built to streamline charity workflows:  

- 🎯 Create projects with goals (target amount, description, lifecycle tracking)  
- 💸 Accept donations that are **auto-allocated** into open projects  
- 📈 Export reports to **Google Sheets** and manage access via **Google Drive API**  
- 🧠 Keep the API endpoints slim by pushing the **investment logic** into a dedicated service layer  

---

## 🧰 Tech Stack  

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/> <img src="https://img.shields.io/badge/SQLAlchemy-8A2BE2?style=for-the-badge&logo=sqlalchemy&logoColor=white"/> <img src="https://img.shields.io/badge/Alembic-cc9900?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white"/> <img src="https://img.shields.io/badge/Uvicorn-000000?style=for-the-badge&logo=uvicorn&logoColor=white"/> <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/> <img src="https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white"/> <img src="https://img.shields.io/badge/Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white"/> <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white"/> <img src="https://img.shields.io/badge/OpenAPI-6BA539?style=for-the-badge&logo=openapiinitiative&logoColor=white"/>  

---

## ✨ Features  

- 🏗 **Projects & Donations** — define projects (name, description, target sum); donations are distributed until projects are fully funded.  
- 🧠 **Smart investment logic** — donations and projects track `full_amount` and `invested_amount`; funds are allocated automatically:  
  - When a project or donation reaches its target, it is marked **fully invested** with a `close_date`.  
  - Distribution stops once either side is satisfied.  
  - Keeps endpoints slim — logic is in `services/investment.py`.  
- 📈 **Google Sheets reports** — generate spreadsheets of top-funded projects and share access through Google Drive.  
- 👤 **Authentication & roles** — users register/authenticate; privileged operations require superuser rights.  
- 🛡 **Clean architecture** — Pydantic schemas, SQLAlchemy models, service layer, CRUD logic.  
- 🔄 **Migrations & testing** — Alembic migrations and a pytest suite with fixtures.  
- 📜 **Interactive API docs** — OpenAPI schema at **/docs** and **/redoc**.  

---

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

