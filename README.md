# 🚨 Login Anomaly Detector

A simple Flask web app to **detect suspicious login attempts** and **send email alerts**.

---

## ✨ Features
- 🔒 Secure user login with username and password
- 📋 Store all login attempts in an SQLite database
- 🕵️ Detect anomalies based on unfamiliar IP addresses
- 📧 Send automatic email alerts for suspicious logins
- 🖥️ Simple, clean frontend to view recent logins and all logs

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/login-anomaly-detector.git
cd login-anomaly-detector
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up the `.env` File
Create a `.env` file in the root directory:
```
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-email-password
TO_EMAIL=recipient-email@example.com
```

*(Tip: You can use Gmail, but you may need to create an "App Password.")*

### 5. Run the Flask App
```bash
python app.py
```

The app will run on:
```
http://127.0.0.1:5000
```

### 6. (Optional) Expose the App to the Internet using ngrok
```bash
ngrok http 5000
```
This will give you a public URL like:
```
https://abc123.ngrok-free.app
```

---

## 📂 Project Structure
```
login-anomaly-detector/
│
├── app.py            # Main Flask app
├── models.py         # Database models
├── utils.py          # Utility functions (anomaly detection, email sending)
├── templates/
│   └── index.html    # Frontend HTML
├── requirements.txt  # Python dependencies
├── .env              # (You create this) Email credentials
└── README.md         # Project documentation
```

---

## 🤔 Future Improvements
- Add user signup/login system (authentication)
- Make anomaly detection smarter (Geo-location, Device fingerprinting)
- Add real-time notifications (Telegram/Slack integration)
- Host on a cloud server (AWS, Heroku)

---

## 💬 Contributing
Feel free to fork this repo, make changes, and open pull requests!

---

**Built with ❤️ by [Sri Charan, Paul Andrew, Kaushal, Janarthanan]**

---

