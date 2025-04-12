import sqlite3
import random
from faker import Faker
from werkzeug.security import generate_password_hash

fake = Faker()

# Create or connect to SQLite database
conn = sqlite3.connect("instance/db.sqlite3")
cursor = conn.cursor()


# Define known values for valid entries
valid_ip_address = [fake.ipv4() for _ in range(50)]
valid_user_agent = ['Chrome', 'Firefox', 'Safari', 'Edge']
valid_location = ['Chennai', 'Mumbai', 'Delhi', 'Bangalore']
valid_users = []
used_usernames = set()

while len(valid_users) < 800:
    username = 'user' + str(len(valid_users))
    if username not in used_usernames:
        password = 'pass' + str(len(valid_users))
        valid_users.append((username, password))
        used_usernames.add(username)

data = []
data1 = []

# Create valid entries
for login, password in valid_users:
    entry = (
        random.choice(valid_ip_address),
        random.choice(valid_user_agent),
        random.choice(valid_location),
        login,
        True  # not anomaly
    )
    entry1 = (
        login,
        generate_password_hash(password),
        password
    )
    data.append(entry)
    data1.append(entry1)

# Generate 200 unique anomaly users
while len(data) < 1000:
    username = fake.user_name()
    if username in used_usernames:
        continue
    used_usernames.add(username)
    password = fake.password()
    entry = (
        fake.ipv4(),
        random.choice(['Opera', 'Brave', 'Unknown']),
        fake.city(),
        username,
        False  # anomaly
    )
    entry1 = (
        username,
        generate_password_hash(password),
        password
    )
    data.append(entry)
    data1.append(entry1)

# Shuffle data to mix normal and anomaly
random.shuffle(data)
random.shuffle(data1)

# Insert into DB
cursor.executemany('''
INSERT INTO login_attempt (ip_address, user_agent, location, username, success)
VALUES (?, ?, ?, ?, ?)
''', data)

cursor.executemany('''
INSERT INTO user (username, password_hash, email)
VALUES (?, ?, ?)
''', data1)

# Commit and close
conn.commit()
conn.close()

print("✅ 1000 login entries (valid + anomalies) dumped into instance/db.sqlite3")
