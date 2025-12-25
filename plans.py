from datetime import datetime, timedelta

PLANS = {
    "FREE": {
        "daily_limit": 0,
        "accounts": 1,
        "duration": None
    },
    "NORMAL": {
        "daily_limit": 75,
        "accounts": 3,
        "duration": 2
    },
    "PREMIUM": {
        "daily_limit": 150,
        "accounts": 7,
        "duration": 3
    },
    "SUPER_PREMIUM": {
        "daily_limit": 300,
        "accounts": 999,
        "duration": 7
    }
}

def calculate_expiry(plan):
    if PLANS[plan]["duration"] is None:
        return None
    return datetime.utcnow() + timedelta(days=PLANS[plan]["duration"])
