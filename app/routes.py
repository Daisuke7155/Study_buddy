# app/routes.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/home')
def home():
    return render_template('home.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.interests = form.interests.data
        current_user.qualifications = form.qualifications.data
        current_user.education = form.education.data
        current_user.work_experience = form.work_experience.data
        current_user.skills = form.skills.data
        current_user.learning_interests = form.learning_interests.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.interests.data = current_user.interests
        form.qualifications.data = current_user.qualifications
        form.education.data = current_user.education
        form.work_experience.data = current_user.work_experience
        form.skills.data = current_user.skills
        form.learning_interests.data = current_user.learning_interests
    return render_template('profile.html', title='Profile', form=form)
