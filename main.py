from datetime import datetime
import src.timeout as timeout
import src.discord as discord
import my_secrets.webhooks as webhooks

import aloe.sensor as sensor
import aloe.message as message

def main():
    # When the Raspberry Pi is rebooted, it should automatically start the main script an display this message:
    try:
        discord.send_to_discord(webhooks.piprojects, "System rebooted")
    except Exception as e:
        print(f"Failed to send reboot message: {e}")
    
    hourly_data = []
    daily_data = []

    while True:
        try:
            # Always sleep to next whole minute
            timeout.sleep_until(timeout.next_min())

            # Collect data every minute from 01 to 60
            data = sensor.get_data()
            if data is not None and data.get("Moisture") is not None:
                sensor.store_data(data)
                hourly_data.append(data["Moisture"])
            else:
                print("Warning: Failed to read sensor data")

            # Create hourly summary
            if datetime.now().minute == 0:
                if len(hourly_data) > 0:
                    summary = sensor.get_summary(hourly_data)
                    sensor.store_summary(summary)
                    hour = datetime.now().hour
                    if hour == 0: hour = 24  # Adjust hour for midnight
                    daily_data.append({"hour": hour, "moisture": summary["Median Moisture(%)"]})  # Collect data every hour from 01 to 24
                else:
                    print(f"Warning: No data collected for hour {datetime.now().hour}")
                hourly_data = []  # Temporary readings deleted every hour

                # Send Discord update at midnight
                if datetime.now().hour == 0:
                    if len(daily_data) > 0:
                        content = message.create_message(daily_data)
                        discord.send_to_discord(webhooks.aloe, content)
                    else:
                        print("Warning: No daily data to send")
                    daily_data = []  # Temporary readings deleted every day
                    daily_data.append({"hour": 0, "moisture": summary["Median Moisture(%)"]})  # Add midnight reading
                
        except Exception as e:
            print(f"Error in main loop: {e}")
            # Continue running instead of crashing

main()
