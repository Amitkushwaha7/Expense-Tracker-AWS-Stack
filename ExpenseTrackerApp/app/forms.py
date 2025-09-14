from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField, TextAreaField
from wtforms import FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange, Regexp
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required')])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=140)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    category = SelectField('Category', choices=[
        ('food', 'Food & Dining'),
        ('shopping', 'Shopping'),
        ('housing', 'Housing'),
        ('transportation', 'Transportation'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        ('healthcare', 'Healthcare'),
        ('personal', 'Personal'),
        ('education', 'Education'),
        ('travel', 'Travel'),
        ('other', 'Other')
    ])
    description = TextAreaField('Description', validators=[Length(max=256)])
    submit = SubmitField('Add Expense')

class BudgetForm(FlaskForm):
    budget = FloatField('Monthly Budget', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Set Budget')

class EditProfileForm(FlaskForm):
    full_name = StringField('Full name', validators=[Length(max=120)])
    bio = TextAreaField('Bio', validators=[Length(max=256)])
    avatar = FileField('Profile photo')
    submit = SubmitField('Save changes')

class CategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired(), Length(min=2, max=64)])
    color = StringField('Color (hex, optional)', validators=[Length(max=16), Regexp(r'^#?[0-9A-Fa-f]{3,6}$', message='Use a hex like #ff9900 or f90')], default='#4e73df')
    submit = SubmitField('Add category')