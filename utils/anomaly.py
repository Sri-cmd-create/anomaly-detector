def calculate_risk_score(current_login, previous_login):
    risk = 0
    if current_login["location"] != previous_login["location"]:
        risk += 50  # Add risk if location has changed
    if current_login["time_diff"] > 60:  # Last login was more than an hour ago
        risk += 30
    return risk


def detect_anomaly(data):
    # simple fake detection for now
    if data.get('ip') == '127.0.0.1':
        return False  # no anomaly
    return True  # anomaly detected
