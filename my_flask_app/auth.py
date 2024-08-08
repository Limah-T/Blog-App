import functools
from flask import Blueprint, render_template, url_for, redirect, flash
from .forms import SignupForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from .models import User
from my_flask_app import db
from my_flask_app import login_manager
from random import randint
import hashlib
from urllib.parse import urlencode


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get_or_404(id)


def login_required(func):
    @functools.wraps(func)
    def decorated_message(*args, **kwargs):
        if not current_user.is_authenticated:
            flash(message='You need to log in or signup to create, edit, comment, create post, edit post or delete a post.', category="error")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_message


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email_exist = db.session.execute(db.select(User).where(User.email == form.email.data.lower())).scalar()
        name_exist = db.session.execute(db.select(User).where(User.name == form.username.data.lower())).scalar()
        if email_exist:
            flash("Email already exist, try to login instead", category="error")
            return render_template('signup.html', form=form, email_exist=True)
        elif name_exist:
            flash("Name has been used, change to another name", category="error")
            three_nums = []
            chosen_nums = ""
            start = True
            while start:
                for n in range(3):
                    random_num = randint(1, 9)
                    three_nums.append(random_num)
                for i in three_nums:
                    chosen_nums += str(i)
                suggested_name = f"{name_exist.name}_{chosen_nums}"
                all_names = db.session.execute(db.select(User).order_by(User.name)).scalars().all()
                print(all_names)
                for x in all_names:
                    print(x.name)
                    if suggested_name in x.name:
                        start = True
                    else:
                        start = False
                return render_template("signup.html", form=form, suggested_name=suggested_name)
        else:
            hashed_password = generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)
            print(hashed_password)

            new_user = User(
                name = form.username.data.lower(), email=form.email.data.lower(), password=hashed_password)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Logged In!", category="success")
            return redirect(url_for('views.home'))

    return render_template('signup.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_exist = db.session.execute(db.select(User).where(User.email == form.email.data.lower())).scalar() or db.session.execute(db.select(User).where(User.name == form.email.data.lower())).scalar()
        if user_exist:
            checking_password = check_password_hash(pwhash=user_exist.password, password=form.password.data)
            if checking_password:
                login_user(user_exist, remember=True)
                return redirect(url_for('views.home'))
            flash("Incorrect password, try again", category="error")
            return render_template('login.html', form=form)
        flash("Email or Username does not exist! try to sign up", category="error")
        return render_template('login.html', form=form, invalid_email=True)
    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash(message="You have been logged out!", category="success")
    return redirect(url_for('views.home'))

