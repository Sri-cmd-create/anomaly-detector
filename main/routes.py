from flask import Blueprint, render_template, request, redirect, url_for, session
from main import main
from models import db, LoginAttempt, User
from utils.anomaly import detect_anomaly
from utils.email import send_email_alert
from datetime import datetime

# main = Blueprint('main', __name__)

def is_logged_in():
    return 'user_id' in session

@main.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('auth.login'))

    logins = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).limit(5).all()
    return render_template('index.html', logins=logins)

from flask_login import login_required, current_user

@main.route('/dashboard')
@login_required
def dashboard():
    attempts = LoginAttempt.query.filter_by(username=current_user.username).order_by(LoginAttempt.timestamp.desc()).all()
    return render_template('dashboard.html', login_attempts=attempts)


@main.route('/login_attempt', methods=['POST'])
def login_attempt():
    if not is_logged_in():
        return redirect(url_for('auth.login'))

    username = request.form['username']
    ip_address = request.remote_addr
    timestamp = datetime.now()

    login = LoginAttempt(username=username, ip_address=ip_address, timestamp=timestamp)
    db.session.add(login)
    db.session.commit()

    user_logins = LoginAttempt.query.filter_by(username=username).all()
    known_ips = {l.ip_address for l in user_logins}

    if detect_anomaly(ip_address, known_ips):
        user = User.query.filter_by(username=username).first()
        if user:
            send_email_alert(
                user.email,
                "Login Anomaly Detected!",
                f"Suspicious login detected for {username} from IP {ip_address} at {timestamp}"
            )

    return redirect(url_for('main.base'))


@main.route('/view_logs')
def view_logs():
    if not is_logged_in():
        return redirect(url_for('auth.login'))

    logs = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).all()
    return render_template('logs.html', logs=logs)
