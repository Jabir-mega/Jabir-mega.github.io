# This file handles the authentication routes for the Flask application including login, logout, and sign-up functionality.

from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# blueprint is a way to organize routes in Flask applications, allowing us to group related routes together.
# It helps in structuring the application and makes it easier to manage routes, especially in larger applications.

# This files is a blueprint of our project which means it stores url paths 

# name of our auth blueprint
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password or email. Try again', category='error')
        else:
            flash('email does not exist', category='error')
    return render_template("login.html", user=current_user )

@auth.route('/logout')
@login_required   
def lagout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up',methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='errror')
        elif len(email) < 10:
            flash("Email address must be valid and greater than 10 characters", category='error')
        elif len(first_name) < 2:
            flash("first name should be greater than 2 characters", category='error')
        elif len(password1) < 7:
            flash("Password must be greater than 7 characters", category='error')
        elif password1 != password2:
            flash("Passwords do not match. Try again", category='error')
        else:
            # add user to the database
            new_user = User(email = email, first_name = first_name, password=generate_password_hash(password1, method= 'pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            # login_user(user)
            flash("Account created", category=' success')

            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)