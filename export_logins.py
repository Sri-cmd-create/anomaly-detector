import pandas as pd

# Reconnect to the database
conn = sqlite3.connect("login_data.db")

# Read from the logins table into a DataFrame
df = pd.read_sql_query("SELECT * FROM logins", conn)

# Export to CSV
df.to_csv("login_data.csv", index=False)

conn.close()

print("✅ Data exported to login_data.csv")
