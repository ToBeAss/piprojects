import time
import sensor
from aloe import sensor

minute = 0
hourly_data = []

while minute < 60:
    try:
        time.sleep(60)
        data = sensor.get_data()
        hourly_data.append(data["Moisture"])
        minute += 1
    except Exception as e:
        print(f"Error in test_sensor loop: {e}")
        # Continue running instead of crashing

summary = sensor.get_summary(hourly_data)
print(summary)