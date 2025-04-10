def otp_is_valid(otp, user):
    return otp == "123456"  # Simplified example

def is_trusted_device(user_id, token):
    return False  # Placeholder logic

def check_2fa_attempt_limit(user_id):
    return True  # Placeholder logic
