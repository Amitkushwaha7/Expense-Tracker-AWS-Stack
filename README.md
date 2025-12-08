# Cloud-Native Personal Expense Tracker

## Project Overview
This project is a comprehensive guide to building, deploying, and monitoring a full-stack web application on the cloud. The goal is not just to build an expense tracker, but to master Cloud Infrastructure and DevOps practices using AWS.

**Key Objectives:**
1.  **Development**: Build a Flask-based web application.
2.  **Database Management**: Connect to a managed cloud database (AWS RDS).
3.  **Deployment**: Host the application on a virtual server (AWS EC2).
4.  **Observability**: Set up real-time monitoring and alerts (AWS CloudWatch).

---

## Architecture & Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, Bootstrap 5 | User Interface for tracking expenses |
| **Backend** | Python (Flask) | API logic and routing |
| **Database** | AWS RDS (PostgreSQL) | Managed cloud storage for production data |
| **Compute** | AWS EC2 (Ubuntu) | Virtual server (VPS) to host the application |
| **Server** | Gunicorn + Nginx | Production-grade application server & reverse proxy |
| **Monitoring** | AWS CloudWatch + SNS | CPU load monitoring and email alerts |

---

## Implementation Roadmap

### Phase 1: Local Development (Completed)
- Built the MVP using Flask and SQLite.
- Implemented Add, Edit, Delete, and View functionalities.
- Created a responsive UI with Bootstrap.

### Phase 2: Cloud Database Setup (AWS RDS)
- Provision a PostgreSQL instance on AWS RDS.
- Configure Security Groups to allow connection.
- Migrate the application from local SQLite to remote PostgreSQL.

### Phase 3: Server Provisioning (AWS EC2)
- Launch an Ubuntu EC2 instance.
- Configure SSH access and Network Security (Firewall).
- Set up the Linux environment (Python, Pip, Virtualenv).

### Phase 4: Production Deployment
- Deploy code to the EC2 server.
- Configure Gunicorn to serve the Python app.
- (Optional) Set up Nginx as a reverse proxy for better performance.

### Phase 5: Monitoring & Alerting
- Set up AWS CloudWatch to track CPU utilization.
- Create an SNS Topic to send email alerts if the server load exceeds 70%.
- Perform stress testing to verify alerts.

---

## Local Setup Instructions

To run the application locally for development:

1.  **Navigate to the app directory**:
    ```bash
    cd expense-tracker
    ```
2.  **Create virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the app**:
    ```bash
    python app.py
    ```
5.  **Access**: Open `http://localhost:5000`

---

## Project Details
- **Project Structure**:
    - `expense-tracker/`: Application source code.
    - `implementation_plan.md`: Step-by-step execution guide.
- **Author**: Amit Kumar
- **Status**: Work in Progress (Phase 2)
