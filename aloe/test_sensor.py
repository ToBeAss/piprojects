import time
import sensor
from aloe import sensor

while True:
    try:
        time.sleep(10)
        data = sensor.get_data()
        print(data)
    except Exception as e:
        print(f"Error in test_sensor loop: {e}")
        # Continue running instead of crashing