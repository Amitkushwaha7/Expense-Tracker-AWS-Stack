# >> Comprehensive Implementation Guide: Deploying Expense Tracker on AWS

This document serves as a detailed, step-by-step guide to deploying the **Expense Tracker** application on **AWS**. It covers everything from local preparation to setting up a production-ready cloud environment with **EC2**, **RDS**, and **CloudWatch**.

---

## [ ] Prerequisites

Before starting, ensure you have:
1.  **AWS Account**: A valid account (Free Tier recommended).
2.  **Terminal/Command Line**: PowerShell (Windows) or Terminal (Mac/Linux).
3.  **SSH Client**: Installed (usually comes with Git or standard on Mac/Linux).
4.  **Source Code**: This `expense-tracker` repository.

---

## Phase 1: Local Preparation ->

Ensure the application works locally before moving to the cloud.

1.  **Dependencies**: Check `requirements.txt` includes `psycopg2-binary` (for PostgreSQL) and `gunicorn` (for the production server).
2.  **Environment Variables**: Create a `.env` file locally to manage secrets.
    ```ini
    DATABASE_URI=postgresql://username:password@hostname:5432/dbname
    SECRET_KEY=your-secret-key
    ```
3.  **Test Run**:
    *   Initialize the DB: `python -c "from app import db, app; app.app_context().push(); db.create_all()"`
    *   Run: `python app.py`

---

## Phase 2: Infrastructure Setup (AWS Console) -> 

We will build the network foundation and provision servers.

### Step 1: Network Setup (VPC & Subnets)
1.  **Go to VPC Dashboard** > **Create VPC**.
    *   Name: `ExpenseTracker-VPC`
    *   IPv4 CIDR: `10.0.0.0/16`
2.  **Create Subnets**:
    *   **Public Subnet** (For EC2): CIDR `10.0.1.0/24`, Zone `us-east-1a`.
    *   **Private Subnet A** (For RDS): CIDR `10.0.2.0/24`, Zone `us-east-1a`.
    *   **Private Subnet B** (For RDS redundant): CIDR `10.0.3.0/24`, Zone `us-east-1b`.
3.  **Internet Gateway (IGW)**:
    *   Create IGW (`ExpenseTracker-IGW`) and **Attach** it to your VPC.
4.  **Route Tables**:
    *   **Public Route Table**: Add rule `0.0.0.0/0` -> Target `ExpenseTracker-IGW`. Associate with **Public Subnet**.
    *   **Private Route Table**: No internet route needed initially. Associate with **Private Subnets**.

### Step 2: Database Setup (RDS)
1.  **Go to RDS Dashboard** > **Subnet Groups** > **Create DB Subnet Group**.
    *   Select your VPC and add both **Private Subnets**.
2.  **Create Database**:
    *   Choose **PostgreSQL** > **Free Tier**.
    *   DB Instance Identifier: `expense-tracker-db`.
    *   Master Username: `admin`.
    *   Master Password: `securepassword123` (Save this!).
    *   **Connectivity**:
        *   VPC: `ExpenseTracker-VPC`.
        *   Public Access: **No**.
        *   security Group: Create a new one (`RDS-SG`).

### Step 3: Compute Setup (EC2)
1.  **Go to EC2 Dashboard** > **Launch Instance**.
    *   Name: `ExpenseTracker-Web`.
    *   AMI: **Amazon Linux 2023**.
    *   Instance Type: **t2.micro**.
    *   Key Pair: Create new (`expense-key.pem`) and **download it**.
    *   **Network Settings**:
        *   VPC: `ExpenseTracker-VPC`.
        *   Subnet: **Public Subnet**.
        *   Auto-assign Public IP: **Enable**.
        *   **Security Group**: Create new (`Web-SG`).
            *   Allow **SSH (22)** from **My IP**.
            *   Allow **HTTP (80)** from **Anywhere**.

---

## Phase 3: Security Configuration -> 

Connect the EC2 to the RDS securely.

1.  **Go to VPC** > **Security Groups**.
2.  Select **RDS-SG** (created in Step 2).
3.  **Edit Inbound Rules**:
    *   Type: **PostgreSQL (5432)**.
    *   Source: Select **Custom** and choose the **Web-SG** (the security group of your EC2).
    *   *Result: Only your EC2 server can talk to the database.*

---

## Phase 4: Application Deployment -> 

Deploy the code to the live server.

### Step 1: Connect to EC2
1.  Open Terminal/PowerShell.
2.  Move your key to a safe folder and restrict permissions (Linux/Mac: `chmod 400 expense-key.pem`).
3.  SSH into the instance:
    ```bash
    ssh -i expense-key.pem ec2-user@<PUBLIC-IP-OF-EC2>
    ```

### Step 2: Server Environment Setup
Run these commands inside EC2:
```bash
# Update system
sudo yum update -y

# Install Python, Git, and PostgreSQL tools
sudo yum install python3 git postgresql15 -y

# Clone Repository
git clone https://github.com/YOUR_GITHUB_USER/flask-expense-tracker.git
cd flask-expense-tracker

# Setup Application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Env Variables
Create the `.env` file on the server:
```bash
nano .env
```
Paste your production config (use RDS endpoint from AWS Console):
```ini
DATABASE_URI=postgresql://admin:securepassword123@<RDS-ENDPOINT>:5432/postgres
```
Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

### Step 4: Run with Gunicorn & Nginx
1.  **Test Gunicorn**:
    ```bash
    gunicorn -w 4 -b 0.0.0.0:8000 app:app
    ```
2.  **Install Nginx**:
    ```bash
    sudo yum install nginx -y
    sudo systemctl start nginx
    ```
3.  **Configure Nginx Proxy**:
    Edit `/etc/nginx/nginx.conf` (`sudo nano`) to forward Port 80 to Port 8000.
    ```nginx
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    ```
4.  **Restart Nginx**:
    ```bash
    sudo systemctl restart nginx
    ```

**🎉 Your app is now LIVE at your EC2 Public IP!**

---

## Phase 5: Monitoring & Alerts (CloudWatch) ->

Ensure you know if the server crashes.

1.  **Go to CloudWatch Console** > **Alarms** > **Create Alarm**.
2.  **Select Metric**: EC2 > Per-Instance Metrics > **CPUUtilization**.
3.  **Conditions**: Greater than **80%** for **5 minutes**.
4.  **Actions**:
    *   Trigger: **In Alarm**.
    *   Notification: **Create new topic** (`HighCpuAlerts`).
    *   Email: Enter your email address.
5.  **Create Alarm**.
    *   *Result: You will get an email if your server is overloaded.*

---

### [x] Summary of Achievements
*   **Infrastructure**: VPC, Public/Private Subnets, Security Groups.
*   **Compute & Database**: T2.micro Web Server + Managed RDS Postgres.
*   **Production Server**: Nginx + Gunicorn configuration.
*   **Observability**: Automated CPU alerts via CloudWatch.
