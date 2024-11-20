import time
from datetime import datetime, timedelta

def next_hour():
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    wait = (next_hour - now).total_seconds()
    return wait

def next_min():
    now = datetime.now()
    next_min = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    wait = (next_min - now).total_seconds()
    return wait

def sleep(seconds):
    time.sleep(seconds)