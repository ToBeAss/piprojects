from datetime import datetime
import src.timeout as timeout
import src.discord as discord
import my_secrets.webhooks as webhooks

import aloe.sensor as sensor
import aloe.message as message

def main():
    # When the Raspberry Pi is rebooted, it should automatically start the main script an display this message:
    discord.send_to_discord(webhooks.piprojects, "System rebooted")
    hourly_data = []
    daily_data = []

    while True:
        # Always sleep for a minute
        next_min = timeout.next_min()
        timeout.sleep(next_min)

        # Check if it's a new hour
        if datetime.now().minute == 0:
            summary = sensor.get_summary(hourly_data)
            sensor.store_summary(summary)
            hour = datetime.now().hour
            daily_data.append({"hour": hour, "moisture": summary["Median Moisture(%)"]})  # Collect data every hour from 01 to 24
            hourly_data = []  # Temporary readings deleted every hour

            # Send Discord update at midnight
            if datetime.now().hour == 0:
                content = message.create_message(daily_data)
                discord.send_to_discord(webhooks.aloe, content)
                daily_data = []  # Temporary readings deleted every day

        # Collect data every minute from 00 to 59
        data = sensor.get_data()
        hourly_data.append(data["Moisture"])
        sensor.store_data(data)

main()
