# Personal Expense Tracker - AWS Cloud Project

![AWS Architecture](https://via.placeholder.com/800x400?text=Personal+Expense+Tracker+AWS+Architecture)

## Project Overview
Personal Expense Tracker is a cloud-based application that helps users track and manage their personal expenses. The project demonstrates how to deploy a Flask web application on AWS infrastructure using EC2 for hosting, RDS for database storage, and CloudWatch for monitoring and alerts.

This project serves as a practical learning experience for both application development and cloud infrastructure management.

## Features
- **User Authentication:** Secure registration and login system
- **Expense Management:** Add, view, edit, and delete personal expenses
- **Categorization:** Organize expenses by customizable categories
- **Budget Tracking:** Set monthly budgets and receive alerts when nearing limits
- **Data Visualization:** Visual representations of spending patterns through charts
- **Responsive Design:** Mobile-friendly interface that works across all devices
- **Cloud Infrastructure:** Fully deployed on AWS with scalability in mind
- **Monitoring:** Real-time monitoring with CloudWatch metrics and alerts

## Architecture
![Architecture Diagram](https://via.placeholder.com/600x400?text=Architecture+Diagram)

The application follows a three-tier architecture:

- **Presentation Tier:** Flask web application hosted on EC2
- **Application Tier:** Python business logic running on EC2
- **Data Tier:** PostgreSQL database hosted on Amazon RDS

## AWS Services Used
- **Amazon EC2:** Hosts the Flask web application
- **Amazon RDS:** Provides managed PostgreSQL database service
- **Amazon CloudWatch:** Monitors application performance and sends alerts
- **Amazon VPC:** Provides network isolation for the application components
- **Amazon S3 (optional):** Stores static assets for the application
- **Amazon Route 53 (optional):** Manages domain and DNS routing

## Technologies
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Visualization:** Chart.js
- **Cloud:** AWS (EC2, RDS, CloudWatch)
- **Version Control:** Git, GitHub

## Prerequisites
- AWS Account with appropriate permissions
- Basic knowledge of AWS services (EC2, RDS, CloudWatch)
- Familiarity with Python and Flask
- AWS CLI installed and configured
- Git installed

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Amitkushwaha7/Expense-Tracker-AWS-Stack.git
cd Expense-Tracker-AWS-Stack
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///expense_tracker.db  # For local development
```

### 5. Initialize the Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the Application
```bash
flask run
```

Access the application at [http://localhost:5000](http://localhost:5000)
