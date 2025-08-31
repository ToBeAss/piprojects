import time
from datetime import datetime, timedelta

def next_hour():
    return (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

def next_min():
    return (datetime.now() + timedelta(minutes=1)).replace(second=0, microsecond=0)

def sleep_until(target_time: datetime):
    wait_time = (target_time - datetime.now()).total_seconds()
    time.sleep(wait_time)