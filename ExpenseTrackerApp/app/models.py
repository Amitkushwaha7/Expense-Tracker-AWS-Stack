from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    expenses = db.relationship('Expense', backref='author', lazy='dynamic')
    budget = db.Column(db.Float, default=0.0)
    full_name = db.Column(db.String(120))
    bio = db.Column(db.String(256))
    avatar_path = db.Column(db.String(256))
    categories = db.relationship('Category', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_total_expenses(self):
        """Sum of all expenses for this user."""
        return sum(expense.amount for expense in self.expenses)
    
    def get_budget_remaining(self):
        return self.budget - self.get_total_expenses()

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    amount = db.Column(db.Float)
    category = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(256))
    
    def __repr__(self):
        return f"<Expense {self.title}, ${self.amount}>"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    color = db.Column(db.String(16))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='uq_user_category_name'),)

    def __repr__(self):
        return f"<Category {self.name}>"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))