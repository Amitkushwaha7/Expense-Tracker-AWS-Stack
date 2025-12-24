# Expense Tracker App – Cloud Deployed

This is a cloud-deployed expense tracker web application built using **Flask**, hosted on **AWS EC2**, and connected to a **PostgreSQL RDS** database.

It allows users to organize expenses through a simple and clean web interface, featuring:
- Add, edit, and delete expenses
- Filter by category, payment method, user, and date range
- View summary totals

---

### >> Phase 1: Cloud Deployment

In this phase, I focused on:
- Setting up a secure and scalable cloud environment using **AWS VPC**
- Deploying the Flask app on an **EC2 instance** using **Gunicorn** and **Nginx**
- Storing data on a **PostgreSQL RDS instance** in a private subnet
- Logging application activity using **CloudWatch Agent**
- Managing configuration via a `.env` file and **dotenv**

> [x] Successfully deployed the app to the cloud with persistent storage and public access via a public IP.
>
> [!] While a custom domain and HTTPS will be added in future phases, the current setup prioritizes security within budget limits (e.g., private RDS, strict security groups).

---

### [ ] Tech Stack

- **Python (Flask)**
- **PostgreSQL (AWS RDS)**
- **AWS EC2, VPC, Subnets, Security Groups**
- **Gunicorn + Nginx** (for production WSGI setup)
- **python-dotenv** (.env configuration)
- **AWS CloudWatch** (logging)

### [ ] Demo Video

[Watch the Video on YouTube](https://youtu.be/bfRccKXN7mY)

This 2-minute walkthrough demonstrates the app running on AWS EC2 + RDS, including architecture, logging, and live functionality.

---

### >> How to Run Locally

```bash
git clone https://github.com/yourusername/expense-tracker-app.git
cd expense-tracker-app
pip install -r requirements.txt
python app.py
```

---

### >> Deployment Steps (AWS)

This section outlines how I deployed the Flask Expense Tracker App to AWS using EC2 and RDS, with security, scalability, and observability.

#### 1. [ ] Infrastructure Setup (VPC, Subnets, Security Groups)
- Created a **custom VPC** with:
  - 1 public subnet (for EC2 instance)
  - 1 private subnet (for RDS instance)
- Configured **Internet Gateway** and routing tables
- Set up **Security Groups**:
  - EC2 SG: allows SSH (22), HTTP (80), and app port from anywhere
  - RDS SG: only allows inbound traffic from EC2 private IP range

#### 2. [ ] EC2 Instance Setup
- Launched an **Linux EC2 instance** in the public subnet
- Installed:
  - Python, pip, virtualenv
  - Git, PostgreSQL client
- Cloned GitHub repo and set up Python virtual environment
- Installed app dependencies with:
  ```bash
  pip install -r requirements.txt
  ```

#### 3. [ ] Environment Configuration
- Created a `.env` file to store environment variables (e.g. `DATABASE_URI`, `FLASK_ENV`)
- Used `python-dotenv` to load these variables into the Flask app

#### 4. [ ] App Server & Web Server
- Installed Gunicorn to run Flask in production mode:
  ```bash
  gunicorn -w 4 app:app
  ```
- Installed and configured Nginx as a reverse proxy to forward traffic to Gunicorn
- Set up Nginx to serve HTTP on port 80

#### 5. [ ] RDS Setup (PostgreSQL)
- Created a PostgreSQL RDS instance in the private subnet
- Set up database schema and tested connection from EC2 instance
- Verified that all app data is being stored in RDS

#### 6. [ ] Logging & Monitoring
- Installed and configured CloudWatch Agent to stream:
  - Gunicorn logs
  - System metrics (CPU, memory)

#### 7. [ ] Security Considerations
- RDS placed in private subnet — not exposed to the internet
- EC2 access limited to my IP (for SSH)
- Sensitive credentials stored in `.env`, not committed to GitHub
- HTTPS and domain name will be configured in Phase 2 to reduce initial hosting cost

---

### >> Next Phase: Features & Cloud Engineering Enhancements

In the next phase, I’ll focus on strengthening the project’s architecture, automation, and cloud-native integrations:

- **Containerization** – Package the app with Docker for portability and easier deployment
- **Infrastructure as Code** – Use Terraform to automate provisioning of AWS resources
- **CI/CD Pipeline** – Implement GitHub Actions to automate build and deployment
- **Dashboard & Analytics** – Visualize expenses with charts and summaries
- **AI Feature (OCR)** – Integrate AWS Textract to extract text from receipt images
- **Advanced Monitoring** – Set up CloudWatch metrics dashboards and alerting

> These enhancements will further align the project with real-world cloud architecture and DevOps workflows.
