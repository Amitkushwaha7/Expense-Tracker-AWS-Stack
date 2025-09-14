from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
    Response,
)
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Expense, Category
from app.forms import (
    LoginForm,
    RegistrationForm,
    ExpenseForm,
    BudgetForm,
    EditProfileForm,
    CategoryForm,
)
from urllib.parse import urlparse
from datetime import datetime, timedelta, date
import csv
import io

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

# Default categories used as seeds for dropdowns
DEFAULT_CATEGORIES = [
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
]

def _category_choices_for_user(user: User):
    """Merge defaults with a user's custom categories (avoiding duplicate keys)."""
    existing_keys = {key for key, _ in DEFAULT_CATEGORIES}
    choices = list(DEFAULT_CATEGORIES)
    if user:
        for cat in user.categories.order_by(Category.name.asc()).all():
            key = cat.name.strip().lower()
            label = cat.name.strip()
            if key not in existing_keys:
                choices.append((key, label))
    return choices


def _month_bounds(d: date):
    first_of_month = date(d.year, d.month, 1)
    if d.month == 12:
        first_of_next = date(d.year + 1, 1, 1)
    else:
        first_of_next = date(d.year, d.month + 1, 1)
    last_of_month = first_of_next - timedelta(days=1)
    return first_of_month, last_of_month


def _parse_date(text: str | None) -> date | None:
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except Exception:
        return None


def _date_range_from_params(period: str, start_str: str | None, end_str: str | None):
    """Resolve the effective date range based on a period or explicit start/end."""
    today = date.today()
    start_date: date | None = None
    end_date: date | None = None

    if period == "this_month":
        start_date, end_date = _month_bounds(today)
    elif period == "last_30":
        start_date = today - timedelta(days=29)
        end_date = today
    elif period == "this_year":
        start_date = date(today.year, 1, 1)
        end_date = date(today.year, 12, 31)

    # Override with explicit dates if provided and valid
    s = _parse_date(start_str)
    e = _parse_date(end_str)
    if s and e and s <= e:
        start_date, end_date = s, e

    return start_date, end_date

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

# Main routes
@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html', title='Welcome')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Filters: period (this_month, last_30, this_year) or custom start/end
    period = request.args.get('period', 'this_month')
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    start_date, end_date = _date_range_from_params(period, start_str, end_str)

    q = Expense.query.filter_by(user_id=current_user.id)
    if start_date and end_date:
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())
        q = q.filter(Expense.timestamp >= start_dt, Expense.timestamp <= end_dt)

    # Recent 5 expenses in selected range
    expenses = q.order_by(Expense.timestamp.desc()).limit(5).all()

    # Totals in range
    expenses_in_range = q.all()
    total_expenses = sum(e.amount for e in expenses_in_range)
    budget = current_user.budget or 0.0
    budget_remaining = budget - total_expenses

    # Category breakdown
    categories = {}
    for exp in expenses_in_range:
        categories[exp.category] = categories.get(exp.category, 0) + exp.amount

    # Trend over time (daily for <= 60 days, else monthly)
    trend_points = {}
    if start_date and end_date and (end_date - start_date).days <= 60:
        for exp in expenses_in_range:
            key = exp.timestamp.strftime('%Y-%m-%d')
            trend_points[key] = trend_points.get(key, 0) + exp.amount
        trend_labels = sorted(trend_points.keys())
    else:
        for exp in expenses_in_range:
            key = exp.timestamp.strftime('%Y-%m')
            trend_points[key] = trend_points.get(key, 0) + exp.amount
        trend_labels = sorted(trend_points.keys())
    trend_values = [round(trend_points[k], 2) for k in trend_labels]

    # Top categories
    top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]

    return render_template(
        'dashboard.html',
        title='Dashboard',
        expenses=expenses,
        total_expenses=round(total_expenses, 2),
        budget=round(budget, 2),
        budget_remaining=round(budget_remaining, 2),
        categories=categories,
        trend_labels=trend_labels,
        trend_values=trend_values,
        period=period,
        start_date=start_date.strftime('%Y-%m-%d') if start_date else '',
        end_date=end_date.strftime('%Y-%m-%d') if end_date else '',
        top_categories=top_categories,
    )

@main_bp.route('/expenses')
@login_required
def expenses():
    page = request.args.get('page', 1, type=int)
    query = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.timestamp.desc())
    expenses = db.paginate(query, page=page, per_page=10)
    return render_template('expenses.html', title='My Expenses', expenses=expenses)

@main_bp.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    # Dynamic categories for current user
    form.category.choices = _category_choices_for_user(current_user)
    if form.validate_on_submit():
        expense = Expense(title=form.title.data,
                         amount=form.amount.data,
                         category=form.category.data,
                         description=form.description.data,
                         author=current_user)
        db.session.add(expense)
        db.session.commit()
        
        # Check if expense pushes user over budget
        budget_remaining = current_user.get_budget_remaining()
        if budget_remaining < 0:
            # If we were using AWS CloudWatch in production
            # We would send an alert here
            flash('Warning: You have exceeded your budget!', 'warning')
        
        flash('Expense has been added!')
        return redirect(url_for('main.dashboard'))
    return render_template('add_expense.html', title='Add Expense', form=form)


@main_bp.route('/expense/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash('You cannot edit this expense!')
        return redirect(url_for('main.expenses'))

    form = ExpenseForm()
    form.category.choices = _category_choices_for_user(current_user)
    if request.method == 'GET':
        form.title.data = expense.title
        form.amount.data = expense.amount
        # Ensure current category is present in choices
        current_key = (expense.category or 'other').lower()
        if current_key not in [k for k, _ in form.category.choices]:
            label = (expense.category or 'Other').title()
            form.category.choices.append((current_key, label))
        form.category.data = current_key
        form.description.data = expense.description
        # Adjust submit label for UI
        form.submit.label.text = 'Save Changes'

    if form.validate_on_submit():
        expense.title = form.title.data
        expense.amount = form.amount.data
        expense.category = form.category.data
        expense.description = form.description.data
        db.session.commit()
        flash('Expense has been updated!')
        return redirect(url_for('main.expenses'))

    # Reuse add_expense template with edit context
    return render_template('add_expense.html', title='Edit Expense', form=form)

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    budget_form = BudgetForm()
    edit_form = EditProfileForm()
    category_form = CategoryForm(prefix='cat')

    # Handle budget form
    if budget_form.submit.data and budget_form.validate_on_submit():
        current_user.budget = budget_form.budget.data
        db.session.commit()
        flash('Your budget has been updated!')
        return redirect(url_for('main.profile'))

    # Handle edit profile form
    if edit_form.submit.data and edit_form.validate_on_submit():
        current_user.full_name = edit_form.full_name.data
        current_user.bio = edit_form.bio.data

        # Avatar upload handling
        file = edit_form.avatar.data
        if file and getattr(file, 'filename', None):
            if current_app.config.get('READ_ONLY'):
                flash('Running in read-only mode; avatar not saved.', 'warning')
            else:
                from werkzeug.utils import secure_filename
                import os
                filename = secure_filename(file.filename)
                if filename:
                    upload_folder = current_app.config.get('UPLOAD_FOLDER')
                    os.makedirs(upload_folder, exist_ok=True)
                    save_path = os.path.join(upload_folder, filename)
                    file.save(save_path)
                    rel_path = os.path.join('uploads', filename)
                    current_user.avatar_path = rel_path

        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('main.profile'))

    # Handle category form
    if category_form.submit.data and category_form.validate_on_submit():
        name = category_form.name.data.strip()
        color = category_form.color.data.strip() if category_form.color.data else None
        # Normalize color to start with '#'
        if color and not color.startswith('#'):
            color = f'#{color}'
        # Check uniqueness per user
        exists = Category.query.filter_by(user_id=current_user.id, name=name).first()
        if exists:
            flash('Category already exists.', 'warning')
        else:
            db.session.add(Category(name=name, color=color, owner=current_user))
            db.session.commit()
            flash('Category added!')
        return redirect(url_for('main.profile'))

    if request.method == 'GET':
        budget_form.budget.data = current_user.budget
        edit_form.full_name.data = current_user.full_name
        edit_form.bio.data = current_user.bio

    categories = current_user.categories.order_by(Category.name.asc()).all()
    return render_template('profile.html', title='Profile', budget_form=budget_form, edit_form=edit_form, category_form=category_form, categories=categories)

@main_bp.route('/expense/<int:id>/delete')
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash('You cannot delete this expense!')
        return redirect(url_for('main.expenses'))
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted!')
    return redirect(url_for('main.expenses'))


@main_bp.route('/category/<int:id>/delete')
@login_required
def delete_category(id):
    cat = Category.query.get_or_404(id)
    if cat.user_id != current_user.id:
        flash('You cannot delete this category!')
        return redirect(url_for('main.profile'))
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted!')
    return redirect(url_for('main.profile'))


@main_bp.route('/dashboard/export')
@login_required
def export_expenses():
    period = request.args.get('period', 'this_month')
    start_str = request.args.get('start')
    end_str = request.args.get('end')
    start_date, end_date = _date_range_from_params(period, start_str, end_str)

    q = Expense.query.filter_by(user_id=current_user.id)
    if start_date and end_date:
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())
        q = q.filter(Expense.timestamp >= start_dt, Expense.timestamp <= end_dt)

    rows = q.order_by(Expense.timestamp.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Title', 'Category', 'Amount', 'Description'])
    for r in rows:
        writer.writerow([
            r.timestamp.strftime('%Y-%m-%d %H:%M'),
            r.title,
            r.category,
            f"{r.amount:.2f}",
            r.description or ''
        ])
    csv_data = output.getvalue()
    output.close()

    today = date.today()
    filename = f"expenses_{today.strftime('%Y%m%d')}.csv"
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename={filename}'
        }
    )