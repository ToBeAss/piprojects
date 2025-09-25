import time
import sys
import os

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aloe import sensor

while True:
    try:
        data = sensor.get_data()
        print(data)
        time.sleep(10)
    except Exception as e:
        print(f"Error in test_sensor loop: {e}")
        # Continue running instead of crashing