# unbound-summer-intern
# Command Gateway Backend

A backend system for controlling command execution using rules, credits, and audit logs.

---

## **Tech Stack**

- **Backend:** Python 3.12, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **API Documentation / Testing:** Swagger UI (built-in FastAPI `/docs`)
- **Authentication:** API Key per user
- **Frontend:** Optional simple HTML/CSS/JS interface

---

## **Setup**

1. **Clone repository:**

```bash
git clone <your_repo_link>
cd backend


2. **Install dependencies:**

```bash
pip install -r requirements.txt

3. **Configure PostgreSQL database:**

- Create a database (example: unbound) using pgAdmin or psql.
- Update .env file with your database credentials:

```bash
DB_USER=postgres
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=unbound
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/unbound


4. **Run the server:**

```bash
uvicorn backend.app.main:app --reload


Swagger UI available at: http://127.0.0.1:8000/docs
