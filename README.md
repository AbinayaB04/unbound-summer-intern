# unbound-summer-intern
# Command Gateway Backend

A backend system for controlling command execution using rules, credits, and audit logs.

---

## **Tech Stack**

* **Backend:** Python 3.12, FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **API Documentation / Testing:** Swagger UI (built-in FastAPI `/docs`)
* **Authentication:** API Key per user
* **Frontend:** Optional simple HTML/CSS/JS interface

---

## **Setup**

1.  **Clone repository:**

    ```bash
    git clone <your_repo_link>
    cd backend
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure PostgreSQL database:**

    * Create a database (example: `unbound`) using pgAdmin or psql.
    * Update `.env` file with your database credentials:

    ```ini
    DB_USER=postgres
    DB_PASS=your_password
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=unbound
    DATABASE_URL=postgresql://postgres:your_password@localhost:5432/unbound
    ```

4.  **Run the server:**

    ```bash
    uvicorn backend.app.main:app --reload
    ```

    > **Swagger UI available at:** `http://127.0.0.1:8000/docs`

---

## **Features**

### **Users**

* Admins can create users and view all users.
* Each user has:
    * `name`
    * `role` (admin or member)
    * `credits`
    * `API key` (for authentication)

### **Rules**

* Admins can add rules with regex patterns and actions:
    * `AUTO_ACCEPT` → Command executes automatically
    * `AUTO_REJECT` → Command rejected
    * `REQUIRE_APPROVAL` → Pending until approved

* Example rules:

    ```bash
    :(){ :|:& };:          → AUTO_REJECT (Fork bomb)
    rm\s+-rf\s+/           → AUTO_REJECT (Force remove root directory)
    mkfs\.                 → AUTO_REJECT (File system creation)
    git\s+(status|log|diff) → AUTO_ACCEPT (Safe Git commands)
    ^(ls|cat|pwd|echo)     → AUTO_ACCEPT (Basic system commands)
    ```

### **Commands**

* Members can submit commands.
* Commands are checked against rules.
* Credits are required to execute commands.
* Commands are logged in the audit trail.
* If user credits $\le 0$ → command rejected.

---

## **Audit Logs**

All significant actions within the system are logged:

* **Command status:** Executed, rejected, or pending.


---

## **Swagger UI Usage**

To interact with the API using the Swagger documentation:

1.  Open the following URL in your browser: `http://127.0.0.1:8000/docs`
2.  Authenticate using the **`X-API-Key`** header with a valid user's API key.

### Available Endpoints for Testing:

* `/users/` → Create or list users.
* `/rules/` → Add or list rules.
* `/commands/` → Submit or list user commands.
* `/logs/` → View audit logs (**Admin Only**).

---

## **Frontend (Optional)**

A simple HTML/CSS/JS form is available to facilitate easy testing and administration:

* **Command Execution:** Enter your API key and a command to execute.
* **Admin Features:**
    * Add users (Admin only).
    * Add rules (Admin only).
    * View logs and commands.

> **Goal:** The frontend features minimal styling and provides a clear form structure for quick and easy testing of the core functionalities.

---

## 💡 Notes

* **Transactional Actions:** All actions (e.g., command submission) are transactional. Credit deduction and log creation occur **atomically**.
* **API Key Authentication:** Every request to the API **must** include the `X-API-Key` header for authentication.
* **Executed Commands:** Commands that are executed will still result in a deduction of **1 credit**.

### ✨ Bonus Features Implemented

* **Rule Conflict Detection:** Logic is implemented to prevent the creation of rules with overlapping patterns.
* **Frontend Command Submission:** The optional frontend is functional for submitting commands.

### Demo link
<https://www.loom.com/share/7a8b71e861b946d481de23dbdf7903ee>
<https://www.loom.com/share/614df4d8762043aa829ce6931dd8c0c9>
