import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import pickle
from datetime import datetime

# Step 1: Read Data from Database
def load_data(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT username, ip_address, user_agent, location, timestamp FROM login_attempt"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Step 2: Preprocess Data
def preprocess_data(df):
    # Fill missing values if any
    df = df.fillna("unknown")

    # Label Encoding
    ip_encoder = LabelEncoder()
    browser_encoder = LabelEncoder()
    location_encoder = LabelEncoder()

    df['ip_encoded'] = ip_encoder.fit_transform(df['ip_address'])
    df['browser_encoded'] = browser_encoder.fit_transform(df['user_agent'])
    df['location_encoded'] = location_encoder.fit_transform(df['location'])

    # Convert timestamp to hour
    df['hour'] = pd.to_datetime(df['timestamp'], errors='coerce').dt.hour.fillna(0).astype(int)

    X = df[['ip_encoded', 'browser_encoded', 'location_encoded', 'hour']]

    return X, ip_encoder, browser_encoder, location_encoder

# Step 3: Train Isolation Forest
def train_model(X):
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    return model

# Step 4: Save Model and Encoders
def save_model(model, ip_encoder, browser_encoder, location_encoder):
    with open('isolation_forest_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    with open('encoders.pkl', 'wb') as f:
        pickle.dump((ip_encoder, browser_encoder, location_encoder), f)

# Main Function
def main():
    db_path = 'instance/db.sqlite3'  # <== CHANGE THIS if your db file is named differently

    print("Loading data...")
    df = load_data(db_path)

    print(f"Data loaded: {len(df)} records")

    print("Preprocessing data...")
    X, ip_encoder, browser_encoder, location_encoder = preprocess_data(df)

    print("Training model...")
    model = train_model(X)

    print("Saving model and encoders...")
    save_model(model, ip_encoder, browser_encoder, location_encoder)

    print("✅ Done! Model and encoders are saved.")

if __name__ == "__main__":
    main()
