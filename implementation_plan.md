# Personal Expense Tracker Implementation Plan

## Project Overview
**Goal**: Build a web application to track daily expenses and income, hosted on the cloud with a managed database, and monitored for performance issues.

## Tech Stack
- **Frontend**: HTML/CSS (Bootstrap or Tailwind) + JavaScript.
- **Backend**: Python (Flask).
- **Database**: AWS RDS (PostgreSQL).
- **Hosting**: AWS EC2 (Ubuntu).
- **Monitoring**: AWS CloudWatch.

---

## Phase 1: Local Development (Build the MVP)
**Goal**: Get the application running on your laptop using SQLite.

1. **Set up the Environment**
   - Create project folder: `expense-tracker`
   - Set up virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # (Windows: venv\Scripts\activate)
     pip install flask flask-sqlalchemy psycopg2-binary
     ```

2. **Database Model (Local)**
   - Use SQLite locally.
   - Model fields: `id`, `title`, `amount`, `category`, `date`.

3. **Create the API & Frontend**
   - **Backend (`app.py`)**:
     - `POST /add`: Add new expense.
     - `GET /`: View all expenses.
     - `DELETE /delete/<id>`: Remove expense.
   - **Frontend (`templates/index.html`)**:
     - Simple form to input expenses.
     - Table to display expenses (Jinja2).

4. **Test Locally**
   - Run `python app.py`.
   - Verify add/delete on `localhost:5000`.

---

## Phase 2: Cloud Database Setup (AWS RDS)
**Goal**: Switch storage from local SQLite to AWS RDS.

1. **Create Security Group for RDS**
   - Name: `RDS-Security-Group`
   - Inbound Rules: PostgreSQL (Port 5432) - Source: My IP (temporary).

2. **Launch RDS Instance**
   - Standard Create -> PostgreSQL -> Free Tier.
   - Master username: `admin`.
   - Public Access: Yes (temporary).
   - Security Group: `RDS-Security-Group`.

3. **Connect Local App to RDS**
   - Get Endpoint URL.
   - Update `app.py`:
     ```python
     # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:PASSWORD@ENDPOINT:5432/postgres'
     ```
   - Run app locally to test connection.

---

## Phase 3: Server Setup (AWS EC2)
**Goal**: Move application code to the cloud.

1. **Launch EC2 Instance**
   - OS: Ubuntu Server 24.04 LTS.
   - Type: t2.micro or t3.micro.
   - Key Pair: `expense-key.pem`.
   - Network: Allow HTTP (Internet) and SSH (Anywhere/My IP).

2. **SSH into EC2**
   - `ssh -i "expense-key.pem" ubuntu@<EC2-PUBLIC-IP>`

3. **Prepare the Server**
   - Update: `sudo apt update && sudo apt upgrade -y`
   - Install deps: `sudo apt install python3-pip python3-venv nginx -y`

---

## Phase 4: Deployment
**Goal**: Deploy code to EC2.

1. **Transfer Code**
   - Git clone: `git clone https://github.com/your-username/expense-tracker.git`
   - `cd expense-tracker`

2. **Install Dependencies**
   - Create venv and install requirements.
   - `pip install gunicorn`

3. **Production Security Update**
   - Edit `RDS-Security-Group` to allow access only from EC2 Private IP/Security Group.
   - Update `app.py` database URL if needed.

4. **Run the App (Production Mode)**
   - `gunicorn --bind 0.0.0.0:5000 app:app`
   - Access via `<EC2-PUBLIC-IP>:5000`.

---

## Phase 5: Monitoring (AWS CloudWatch)
**Goal**: Add CPU/Memory alerts.

1. **Create a Topic (SNS)**
   - Name: `Admin-Alerts`.
   - Subscription: Email.

2. **Create a CloudWatch Alarm**
   - Metric: EC2 -> Per-Instance Metrics -> CPUUtilization.
   - Threshold: > 70%.
   - Action: Trigger `Admin-Alerts`.

3. **Stress Test (Optional)**
   - `sudo apt install stress`
   - Spike CPU to verify alert.
