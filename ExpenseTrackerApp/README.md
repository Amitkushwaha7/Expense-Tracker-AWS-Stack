# ExpenseTracker (Flask)

Track what you spend, set a monthly budget, and see clear charts of where your money goes. Clean UI, small codebase, easy to run.

## Features
- Accounts: sign up/in/out
- Expenses: add, edit, delete
- Categories: built-in + your own
- Budget: monthly total + remaining
- Dashboard: category pie + trend
- Export: CSV for the selected period
- Profile: name, bio, optional avatar

## Quickstart
Local (Python 3.11+):
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows (Git Bash)
pip install -r requirements.txt
python run.py
```
Open http://localhost:5000
 

## Configuration (env)
- `DATABASE_URL` — SQLAlchemy URL (defaults to SQLite)
- `SECRET_KEY` — Flask secret (a dev fallback is used if unset)
- `READ_ONLY=1` — block file writes (avatars) for demo mode (default)

## Project layout
- `app/` — models, forms, routes, templates, static
- `config.py` — app settings
- `run.py` — dev entrypoint
- `requirements.txt`
