import datetime, time
import src.timeout as timeout
import src.discord as discord
import my_secrets.webhooks as webhooks

import aloe.sensor as sensor
import aloe.message as message

def main():
    # When the Raspberry Pi is rebooted, it should automatically start the main script an display this message:
    discord.send_to_discord(webhooks.piprojects, "System rebooted")
    temp = []
    
    while True:
        # Always sleep for a minute
        next_min = timeout.next_min()
        timeout.sleep(next_min)

        # Check if it's a new hour
        if datetime.now().minute == 0:
            summary = sensor.get_summary(temp)
            sensor.store_summary(summary)
            result = summary["Median Moisture(%)"]
            content = message.create_message(result)
            discord.send_to_discord(webhooks.aloe, content)
            temp = []  # Temporary readings deleted every hour

        # Collect data every minute
        data = sensor.get_data()
        temp.append(data["Moisture"])
        sensor.store_data(data)

main()
