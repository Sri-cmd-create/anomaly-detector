from flask import Blueprint, current_app, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
import numpy as np
import pandas as pd
from auth import auth
from models import db, LoginAttempt, User
from werkzeug.security import generate_password_hash, check_password_hash
from utils.anomaly import detect_anomaly
# from utils.email import send_email_alert
from datetime import datetime 
from utils.geo import get_location_from_ip
from sklearn.preprocessing import LabelEncoder

# auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        #### actual form submission data - start
        # ip_address = request.form.get('ip', request.remote_addr)
        # user_agent = request.form.get('browser', request.headers.get('User-Agent'))
        # location = request.form.get('loc', get_location_from_ip(ip_address))
        #### actual form submission data - end

        #### fake for abnormal testing - start
        ip_address = "1.1.12.2"
        user_agent = "TEST"
        location = "China"
        #### fake for abnormal testing - end
        timestamp = datetime.now()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            # flash('Logged in successfully!', 'success')

            login = LoginAttempt(username=username, ip_address=ip_address, timestamp=timestamp, user_agent=user_agent, success=True, location=location)
            db.session.add(login)
            db.session.commit()

            # user_logins = LoginAttempt.query.filter_by(username=username).all()
            # known_ips = {l.ip_address for l in user_logins}

            # if detect_anomaly({'ip': ip_address, 'known_ips': known_ips}):
            #     # user = User.query.filter_by(username=username).first()
            #     if user:
            #         # send_email_alert(
            #         #     user.email,
            #         #     "Login Anomaly Detected!",
            #         #     f"Suspicious login detected for {username} from IP {ip_address} at {timestamp}"
            #         # )
            #         flash(f"Suspicious login detected for {username} from IP {ip_address} at {timestamp}", 'error')
            # else:
            #     return redirect(url_for('auth.dashboard'))

            # Label Encoding
            # ip_encoder = LabelEncoder()
            # browser_encoder = LabelEncoder()
            # location_encoder = LabelEncoder()

            model = current_app.isolation_model
            ip_encoder = current_app.ip_encoder
            browser_encoder = current_app.browser_encoder
            location_encoder = current_app.location_encoder

            ip_encoded = ip_encoder.transform([ip_address])[0] if ip_address in ip_encoder.classes_ else -1
            browser_encoded = browser_encoder.transform([user_agent])[0] if user_agent in browser_encoder.classes_ else -1
            location_encoded = location_encoder.transform([location])[0] if location in location_encoder.classes_ else -1
            hour = pd.Timestamp.now().hour

            ### for abnormal login testing- start
            new_data = {
                'ip': ['1.11.11.1.111'],  # New IP
                'browser': ['duckduckgo'],  # New browser
                'location': ['China']  # New location
            }
            new_df = pd.DataFrame(new_data)
            def safe_transform(encoder, value):
                if value[0] in encoder.classes_:
                    return encoder.transform(value)[0]
                else:
                    encoder.classes_ = np.append(encoder.classes_, value[0])
                    return encoder.transform(value)[0]
            ip_encoded = safe_transform(ip_encoder, [new_df['ip'][0]])
            browser_encoded = safe_transform(browser_encoder, [new_df['browser'][0]])
            location_encoded = safe_transform(location_encoder, [new_df['location'][0]])
            ### for abnormal login testing- end

            features = [[ip_encoded, browser_encoded, location_encoded, hour]]
            prediction = model.predict(features)

            if prediction[0] == -1:
                flash('⚠️ Warning: Unusual login activity detected!', 'warning')
            else:
                flash('✅ Login looks normal.', 'success')
                return redirect(url_for('auth.dashboard'))
            
        else:
            flash('Invalid username or password', 'danger')
            login = LoginAttempt(username=username, ip_address=ip_address, timestamp=timestamp, user_agent=user_agent, success=False)
            db.session.add(login)
            db.session.commit()

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

from flask_login import login_required, current_user

@auth.route('/dashboard')
@login_required
def dashboard():
    attempts = LoginAttempt.query.filter_by(username=current_user.username).order_by(LoginAttempt.timestamp.desc()).all()
    return render_template('dashboard.html', login_attempts=attempts)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # if User.query.filter_by(username=username).first():
        #     return render_template('signup.html', message="Username already exists!")
        # if User.query.filter_by(email=email).first():
        #     return render_template('signup.html', message="Email already exists!")

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another one.', 'error')
            return redirect(url_for('auth.signup'))

        # Check if email already exists (optional but good)
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('auth.signup'))

        password_hash = generate_password_hash(password)

        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signup.html')