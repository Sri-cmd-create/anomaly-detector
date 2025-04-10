from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

def is_logged_in():
    return 'user_id' in session

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return render_template('signup.html', message="Username already exists!")
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', message="Email already exists!")

        password_hash = generate_password_hash(password)

        user = User(username=username, email=email, password=password_hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             session['user_id'] = user.id
#             session['username'] = user.username
#             session.permanent = True
#             return redirect(url_for('main.home'))
#         else:
#             return render_template('login.html', message="Invalid username or password")

#     return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
