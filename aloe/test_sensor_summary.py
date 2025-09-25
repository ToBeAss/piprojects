import time
import sys
import os

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aloe import sensor
from src import discord
from my_secrets import webhooks

minute = 0
hourly_data = []

while minute < 60:
    try:
        data = sensor.get_data()
        print(data)
        if data["Moisture"] != 0:
            hourly_data.append(data["Moisture"])
        minute += 1
        time.sleep(1)
    except Exception as e:
        print(f"Error in test_sensor loop: {e}")
        # Continue running instead of crashing

summary = sensor.get_summary(hourly_data)
print(summary)
try:
    discord.send_to_discord(webhooks.piprojects, f"**Hourly Sensor Summary**\n```\n{summary}\n```")
    print("Summary sent to Discord successfully!")
except Exception as e:
    print(f"Failed to send summary to Discord: {e}")
